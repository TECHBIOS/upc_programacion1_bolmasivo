"""
Clase para manejar la generación de boletas electrónicas
"""

import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any
import logging
from config import *
import numpy as np


class BoletaElectronica:
    """
    Clase para generar boletas electrónicas a partir de documentos internos
    """

    def __init__(self):
        """Inicializar el sistema de boletas"""
        self.numero_actual = NUMERO_INICIAL
        self.boletas_generadas = []
        self.documentos_procesados = {}
        self.setup_logging()

    def setup_logging(self):
        """Configurar el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")],
        )
        self.logger = logging.getLogger(__name__)

    def leer_archivo_entrada(self, archivo: str) -> pd.DataFrame:
        """
        Leer archivo de entrada (CSV o Excel) en formato tabular plano con encabezados
        """
        try:
            if archivo.endswith((".xlsx", ".xls")):
                df = pd.read_excel(archivo)
            else:
                raise ValueError(
                    f"Formato de archivo no soportado: {archivo}. Solo se aceptan .xlsx, .xls"
                )

            # Eliminar espacios en los nombres de las columnas
            df.columns = df.columns.str.strip()

            # Validar columnas requeridas
            columnas_requeridas = [
                "SERIE",
                "NUMERO",
                "FECHA",
                "CLIENTE",
                "MONEDA",
                "TOTAL",
                "PRODUCTO",
                "PRECIO",
                "CANTIDAD",
                "IMPORTE",
            ]
            for col in columnas_requeridas:
                if col not in df.columns:
                    raise ValueError(f"Falta la columna requerida: {col}")

            # Mapear a nombres internos
            df_interno = pd.DataFrame(
                {
                    "numero_documento": df["SERIE"].astype(str)
                    + "-"
                    + df["NUMERO"].astype(str),
                    "total_documento": df["TOTAL"],
                    "codigo_item": ["ITEM{:03d}".format(i + 1) for i in range(len(df))],
                    "descripcion_item": df["PRODUCTO"],
                    "cantidad": df["CANTIDAD"],
                    "precio_unitario": df["PRECIO"],
                    "fecha": df["FECHA"],
                    "cliente": df["CLIENTE"],
                    "moneda": df["MONEDA"],
                    "importe": df["IMPORTE"],
                }
            )
            self.logger.info(f"Archivo leído exitosamente: {archivo}")
            self.logger.info(f"Registros encontrados: {len(df_interno)}")
            return df_interno
        except Exception as e:
            self.logger.error(f"Error al leer archivo {archivo}: {str(e)}")
            raise

    def calcular_subtotal_item(self, cantidad: float, precio_unitario: float) -> float:
        """
        Calcular subtotal de un ítem

        Args:
            cantidad: Cantidad del ítem
            precio_unitario: Precio unitario del ítem

        Returns:
            Subtotal calculado
        """
        return cantidad * precio_unitario

    def dividir_item_grande(
        self, item: Dict[str, Any], limite: float
    ) -> List[Dict[str, Any]]:
        """
        Dividir un ítem que excede el límite en partes proporcionales

        Args:
            item: Diccionario con datos del ítem
            limite: Límite máximo por boleta

        Returns:
            Lista de ítems divididos
        """
        subtotal_item = self.calcular_subtotal_item(
            item["cantidad"], item["precio_unitario"]
        )

        if subtotal_item <= limite:
            return [item]

        # Calcular cuántas partes necesitamos
        num_partes = int(subtotal_item / limite) + 1
        cantidad_por_parte = item["cantidad"] / num_partes

        items_divididos = []
        for i in range(num_partes):
            item_dividido = item.copy()
            item_dividido["cantidad"] = cantidad_por_parte
            item_dividido["subtotal"] = self.calcular_subtotal_item(
                cantidad_por_parte, item["precio_unitario"]
            )
            items_divididos.append(item_dividido)

        return items_divididos

    def optimizacion(
        self, items: List[Dict[str, Any]], limite: float
    ) -> List[List[Dict[str, Any]]]:
        """
        Empaquetar por producto: para cada producto, repartir la cantidad en tantas boletas como sea necesario,
        llenando cada una hasta el límite antes de pasar al siguiente producto.
        """
        boletas = []
        for item in items:
            cantidad_restante = item["cantidad"]
            precio_unitario = item["precio_unitario"]
            descripcion = item["descripcion"]
            codigo = item["codigo"] if "codigo" in item else item.get("codigo_item", "")
            # Repartir la cantidad en boletas
            while cantidad_restante > 0:
                # Calcular la cantidad máxima que cabe en una boleta sin exceder el límite
                max_cantidad = min(cantidad_restante, limite // precio_unitario)
                if max_cantidad == 0:
                    # Si ni una unidad cabe, forzar al menos una (para productos caros)
                    max_cantidad = 1
                subtotal = max_cantidad * precio_unitario
                boleta_item = {
                    "codigo": codigo,
                    "descripcion": descripcion,
                    "cantidad": float(max_cantidad),
                    "precio_unitario": float(precio_unitario),
                    "subtotal": float(subtotal),
                }
                # Si la última boleta tiene espacio y es del mismo producto, intenta llenar
                if (
                    boletas
                    and sum(i["subtotal"] for i in boletas[-1]) + subtotal <= limite
                ):
                    boletas[-1].append(boleta_item)
                else:
                    boletas.append([boleta_item])
                cantidad_restante -= max_cantidad
        return boletas

    def generar_formato_Boleta(
        self, items: List[Dict[str, Any]], documento_origen: str
    ) -> Dict[str, Any]:
        """
        Generar una boleta con los ítems proporcionados

        Args:
            items: Lista de ítems para la boleta
            documento_origen: Número del documento interno de origen

        Returns:
            Diccionario con los datos de la boleta
        """
        # Calcular totales
        subtotal = (
            sum(
                item.get(
                    "subtotal",
                    self.calcular_subtotal_item(
                        item["cantidad"], item["precio_unitario"]
                    ),
                )
                for item in items
            )
            / PORCENTAJE_IGV_CALCULO
        )

        igv = subtotal * (PORCENTAJE_IGV / 100)
        total = subtotal + igv

        # Generar número de boleta
        numero_boleta = f"{SERIE_BOLETA}-{self.numero_actual:06d}"
        self.numero_actual += 1

        boleta = {
            "serie": SERIE_BOLETA,
            "numero": numero_boleta,
            "fecha_emision": datetime.now().strftime("%Y-%m-%d"),
            "cliente": DATOS_CLIENTE,
            "items": items,
            "subtotal": round(subtotal, 2),
            "igv": round(igv, 2),
            "total": round(total, 2),
            "documento_origen": documento_origen,
        }

        self.boletas_generadas.append(boleta)
        return boleta

    def procesamiento(self, df_documento: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Procesar un documento interno y generar sus boletas correspondientes

        Args:
            df_documento: DataFrame con los datos del documento

        Returns:
            Lista de boletas generadas para este documento
        """
        numero_doc = df_documento["numero_documento"].iloc[0]
        total_doc = df_documento["total_documento"].iloc[0]

        self.logger.info(f"Procesando documento {numero_doc} con total S/ {total_doc}")

        # Convertir DataFrame a lista de diccionarios
        items = []
        for _, row in df_documento.iterrows():
            item = {
                "codigo": row["codigo_item"],
                "descripcion": row["descripcion_item"],
                "cantidad": float(row["cantidad"]),
                "precio_unitario": float(row["precio_unitario"]),
                "subtotal": self.calcular_subtotal_item(
                    float(row["cantidad"]), float(row["precio_unitario"])
                ),
            }
            items.append(item)

        # Optimizar empaquetado
        boletas_items = self.optimizacion(items, LIMITE_MAXIMO_BOLETA)

        # Generar boletas
        boletas_generadas = []
        for items_boleta in boletas_items:
            boleta = self.generar_boleta(items_boleta, numero_doc)
            boletas_generadas.append(boleta)

        # Registrar documento como procesado
        self.documentos_procesados[numero_doc] = {
            "total_original": total_doc,
            "boletas_generadas": len(boletas_generadas),
            "total_boletas": sum(b["total"] for b in boletas_generadas),
        }

        self.logger.info(
            f"Documento {numero_doc}: {len(boletas_generadas)} boletas generadas"
        )

        return boletas_generadas

    def pre_procesamiento(self, df: str) -> None:
        """
        df: dataframe

        Args:
            archivo_entrada: Ruta del archivo de entrada
        """
        try:
            # Agrupar por documento interno
            documentos = df.groupby("numero_documento")

            self.logger.info(f"Iniciando procesamiento de {len(documentos)} documentos")

            # Procesar cada documento
            for numero_doc, df_documento in documentos:
                self.procesamiento(df_documento)

            # Generar archivos de salida
            self.generar_archivos_salida()

            self.logger.info("Procesamiento completado exitosamente")

        except Exception as e:
            self.logger.error(f"Error en el procesamiento: {str(e)}")
            raise

    def generar_archivos_salida(self) -> None:
        """Generar archivos Excel y JSON por documento interno en la carpeta 'out'"""
        import os

        try:
            out_dir = "out"
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            for boleta in self.boletas_generadas:
                doc = boleta["documento_origen"]
                # Extraer serie y número
                if "-" in doc:
                    serie, numero = doc.split("-", 1)
                else:
                    serie, numero = doc, ""
                nombre_base = f"boleta_{serie}_{numero}"
                archivo_excel = os.path.join(out_dir, f"{nombre_base}.xlsx")
                archivo_json = os.path.join(out_dir, f"{nombre_base}.json")
                # Filtrar boletas de este documento
                boletas_doc = [
                    b for b in self.boletas_generadas if b["documento_origen"] == doc
                ]
                # Preparar datos para Excel
                datos_excel = []
                for b in boletas_doc:
                    serie_numero = b["numero"]
                    fecha = b["fecha_emision"]
                    cliente = (
                        b["cliente"]["nombre"]
                        if isinstance(b["cliente"], dict)
                        else b["cliente"]
                    )
                    moneda = "Soles"
                    total = b["total"]
                    anexo = b["documento_origen"]
                    for item in b["items"]:
                        fila = {
                            "SERIE-NUMERO": serie_numero,
                            "FECHA": fecha,
                            "CLIENTE": cliente,
                            "MONEDA": moneda,
                            "SUBTOTAL": b["subtotal"],
                            "IGV": b["igv"],
                            "TOTAL": total,
                            "ANEXO": anexo,
                            "PRODUCTO": item["descripcion"],
                            "PRECIO": item["precio_unitario"],
                            "CANTIDAD": item["cantidad"],
                            "IMPORTE": item["subtotal"],
                        }
                        datos_excel.append(fila)
                columnas_salida = [
                    "SERIE-NUMERO",
                    "FECHA",
                    "CLIENTE",
                    "MONEDA",
                    "SUBTOTAL",
                    "IGV",
                    "TOTAL",
                    "ANEXO",
                    "PRODUCTO",
                    "PRECIO",
                    "CANTIDAD",
                    "IMPORTE",
                ]
                df_salida = pd.DataFrame(datos_excel, columns=columnas_salida)
                df_salida.to_excel(archivo_excel, index=False)

                # Guardar JSON solo de este documento
                def convertir_a_serializable(obj):
                    if isinstance(obj, dict):
                        return {k: convertir_a_serializable(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convertir_a_serializable(i) for i in obj]
                    elif isinstance(obj, (np.integer, np.int64)):
                        return int(obj)
                    elif isinstance(obj, (np.floating, np.float64)):
                        return float(obj)
                    elif isinstance(obj, (np.ndarray,)):
                        return obj.tolist()
                    else:
                        return obj

                with open(archivo_json, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "boletas": convertir_a_serializable(boletas_doc),
                            "documento": doc,
                            "resumen": {
                                "total_boletas": len(boletas_doc),
                                "fecha_procesamiento": datetime.now().isoformat(),
                            },
                        },
                        f,
                        indent=2,
                        ensure_ascii=False,
                    )
            self.logger.info(f"Archivos generados en carpeta {out_dir}")
        except Exception as e:
            self.logger.error(f"Error al generar archivos de salida: {str(e)}")
            raise

    def generar_resumen(self) -> Dict[str, Any]:
        """
        Generar resumen del procesamiento

        Returns:
            Diccionario con el resumen
        """
        total_boletas = len(self.boletas_generadas)
        total_documentos = len(self.documentos_procesados)

        resumen = {
            "total_boletas_generadas": total_boletas,
            "total_documentos_procesados": total_documentos,
            "documentos_procesados": self.documentos_procesados,
            "fecha_procesamiento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return resumen
