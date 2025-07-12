"""
Programa principal para la emisión masiva de boletas electrónicas
"""

import sys
import os
from boleta_electronica import BoletaElectronica
from config import ARCHIVO_ENTRADA
import logging

def main():
    """
    Función principal del programa
    """
    print("=" * 60)
    print("SISTEMA DE EMISIÓN MASIVA DE BOLETAS ELECTRÓNICAS")
    print("=" * 60)
    
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
        sistema_boletas.procesar_archivo_completo(ARCHIVO_ENTRADA)
        
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
        
        print("📁 ARCHIVOS GENERADOS:")
        print("-" * 40)
        print(f"  • boletas_generadas.csv - Detalle de todas las boletas")
        print(f"  • boletas_generadas.json - Datos completos en formato JSON")
        print(f"  • log_procesamiento.txt - Registro detallado del proceso")
        
        print("\n🎉 ¡Proceso completado! Revisa los archivos generados.")
        
    except Exception as e:
        print(f"\n❌ Error durante el procesamiento: {str(e)}")
        logging.error(f"Error en main: {str(e)}")
        return 1
    
    return 0

def mostrar_ayuda():
    """Mostrar información de ayuda"""
    print("""
USO DEL SISTEMA DE BOLETAS ELECTRÓNICAS
=======================================

1. PREPARACIÓN DEL ARCHIVO DE ENTRADA:
   - El archivo debe llamarse 'DocumentosInternos.xlsx'
   - DEBE seguir OBLIGATORIAMENTE el nuevo formato estructurado:
     * Línea 1: SERIE;NUMERO;FECHA;CLIENTE;MONEDA;TOTAL;PRODUCTO;PRECIO;CANTIDAD;IMPORTE
     * Líneas siguientes: [Serie];[Numero];[Fecha];[Cliente];[Moneda];[Total];[Producto];[Precio];[Cantidad];[Importe]

2. EJECUCIÓN:
   python main.py

3. ARCHIVOS DE SALIDA:
   - boletas_generadas.xlsx: Detalle de todas las boletas generadas
   - boletas_generadas.json: Datos completos en formato JSON
   - log_procesamiento.txt: Registro detallado del proceso

4. CONFIGURACIÓN:
   - Edita config.py para modificar parámetros como:
     * Límite máximo por boleta (actual: S/ 699)
     * Porcentaje IGV (actual: 18%)
     * Datos del cliente
     * Serie de boletas

EJEMPLO DE ARCHIVO DE ENTRADA:
SERIE;NUMERO;FECHA;CLIENTE;MONEDA;TOTAL;PRODUCTO;PRECIO;CANTIDAD;IMPORTE
B001;1;27/06/2025;Industrias SAC;Soles;900.00;Garbanzo;10.00;90.00;900.00

⚠️ IMPORTANTE: El sistema SOLO acepta este formato. Cualquier otro formato será rechazado.
""")

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        mostrar_ayuda()
    else:
        exit_code = main()
        sys.exit(exit_code) 