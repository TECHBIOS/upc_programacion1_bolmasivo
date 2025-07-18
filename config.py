"""
Configuración del sistema de emisión masiva de boletas electrónicas
"""

# Parámetros configurables del sistema
LIMITE_MAXIMO_BOLETA = 699.00  # Límite máximo por boleta en soles
PORCENTAJE_IGV = 18.0  # Porcentaje de IGV (18%)
PORCENTAJE_IGV_CALCULO = 1.18  # importe de IGV calculable

# Datos genéricos del cliente
DATOS_CLIENTE = {
    "nombre": "CLIENTE VARIOS",
    "tipo_documento": "DNI",
    "numero_documento": "00000000",
    "direccion": "DIRECCIÓN GENÉRICA"
}

# Configuración de series y numeración
SERIE_BOLETA = "B001"
NUMERO_INICIAL = 1

# Configuración de archivos
ARCHIVO_ENTRADA = "DocumentosInternos.xlsx"  # o .xlsx
ARCHIVO_LOG = "log_procesamiento.txt"