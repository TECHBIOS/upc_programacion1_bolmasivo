"""
Programa principal para la emisión masiva de boletas electrónicas
"""

import sys
import os
from boleta_electronica import BoletaElectronica
from config import ARCHIVO_ENTRADA
import logging
import pandas as pd

def main():
    """
    Función principal del programa
    """
    print("=" * 60)
    print("SISTEMA DE EMISIÓN MASIVA DE BOLETAS ELECTRÓNICAS")
    print("=" * 60)
    
    print("1. Ingreso manual.")
    print("2. Importacion masiva.")
    print("3. Salir.")
    opcion = int(input("Seleccionar una opción: "))

    match opcion:
        case 1:
            try:
                # Lista para almacenar registros
                registros = []

                # Ingreso de datos
                serie = input("Serie: ")
                numero = input("Numero: ")
                fecha = input("Fecha (YYYY-MM-DD): ")
                cliente = input("Cliente: ")
                moneda = input("Moneda: ")
                producto = input("Producto: ")
                precio = float(input("Precio: "))
                cantidad = float(input("Cantidad: "))
                total = precio * cantidad

                print("Total:", total)

                # Agregar al registro
                registros.append({
                    "SERIE": serie,
                    "NUMERO": numero,
                    "FECHA": fecha,
                    "CLIENTE": cliente,
                    "MONEDA": moneda,
                    "TOTAL": total,
                    "PRODUCTO": producto,
                    "PRECIO": precio,
                    "CANTIDAD": cantidad,
                    "IMPORTE": total
                })

                # Crear DataFrame
                df = pd.DataFrame(registros)

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
                                
                sistema_boletas = BoletaElectronica()
                # Procesar el archivo completo
                print("🔄 Iniciando procesamiento...")
                sistema_boletas.preProcesamiento(df_interno)

                # Generar resumen
                resumen = sistema_boletas.generar_resumen()

                # Mostrar resultados
                print("\n" + "=" * 60)
                print("✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
                print("=" * 60)
                print(f"📊 Total de documentos procesados: {resumen['total_documentos_procesados']}")
                print(f"🧾 Total de boletas generadas: {resumen['total_boletas_generadas']}")
                print(f"📅 Fecha de procesamiento: {resumen['fecha_procesamiento']}")
                
                # Mostrar detalles por documento
                print("\n📋 DETALLES POR DOCUMENTO:")
                print("-" * 40)
                for doc_num, info in resumen['documentos_procesados'].items():
                    print(f"Documento {doc_num}:")
                    print(f"  - Total original: S/ {info['total_original']:.2f}")
                    print(f"  - Boletas generadas: {info['boletas_generadas']}")
                    print(f"  - Total boletas: S/ {info['total_boletas']:.2f}")
                    print()
                                             
                print("\n🎉 ¡Proceso completado! Revisa los archivos generados.")

            except Exception as e:
                print(f"\n❌ Error durante el procesamiento: {str(e)}")
                logging.error(f"Error en main: {str(e)}")
                return 1 
        case 2:
            try:
                # Verificar si existe el archivo de entrada
                if not os.path.exists(ARCHIVO_ENTRADA):
                    print(f"❌ Error: No se encontró el archivo de entrada '{ARCHIVO_ENTRADA}'")
                    print("\nPor favor, asegúrate de que el archivo esté en el directorio del proyecto.")
                    print("Formatos soportados: .csv, .xlsx, .xls")
                    return
                
                # Inicializar el sistema de boletas
                print(f"📁 Leyendo archivo: {ARCHIVO_ENTRADA}")
                sistema_boletas = BoletaElectronica()
                
                # Procesar el archivo completo
                print("🔄 Iniciando procesamiento...")
                df = sistema_boletas.leer_archivo_entrada(ARCHIVO_ENTRADA)
                sistema_boletas.preProcesamiento(ARCHIVO_ENTRADA)
                
                # Generar resumen
                resumen = sistema_boletas.generar_resumen()
                
                # Mostrar resultados
                print("\n" + "=" * 60)
                print("✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
                print("=" * 60)
                print(f"📊 Total de documentos procesados: {resumen['total_documentos_procesados']}")
                print(f"🧾 Total de boletas generadas: {resumen['total_boletas_generadas']}")
                print(f"📅 Fecha de procesamiento: {resumen['fecha_procesamiento']}")
                
                # Mostrar detalles por documento
                print("\n📋 DETALLES POR DOCUMENTO:")
                print("-" * 40)
                for doc_num, info in resumen['documentos_procesados'].items():
                    print(f"Documento {doc_num}:")
                    print(f"  - Total original: S/ {info['total_original']:.2f}")
                    print(f"  - Boletas generadas: {info['boletas_generadas']}")
                    print(f"  - Total boletas: S/ {info['total_boletas']:.2f}")
                    print()
                                             
                print("\n🎉 ¡Proceso completado! Revisa los archivos generados.")
                
            except Exception as e:
                print(f"\n❌ Error durante el procesamiento: {str(e)}")
                logging.error(f"Error en main: {str(e)}")
                return 1
        case 3:
            exit()

    return 0



if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 