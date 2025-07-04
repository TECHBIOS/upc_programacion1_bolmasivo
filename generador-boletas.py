"""
PROGRAMA: GENERADOR DE BOLETAS
Versión: 1.0
Autor: Marcos
Descripción: Divide un documento de ventas en múltiples boletas sin exceder 700 soles por boleta.
"""

# Importar módulo CSV para manejar archivos de datos
import csv

#   Función para leer el archivo CSV con los productos
def leer_documento_interno(archivo_csv):
    """
    Lee un archivo CSV con productos y precios.
    Formato esperado: producto,monto (ejemplo: 'Laptop,600')
    """
    productos = []
    #   Abrir archivo en modo lectura con codificación UTF-8
    with open(archivo_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        #   Saltar la primera fila (encabezado)
        next(reader)  
        for row in reader:
            #   Verificar que la fila tenga al menos 2 columnas
            if len(row) >= 2:  
                producto = row[0].strip()  #   Eliminar espacios del nombre
                monto = float(row[1].strip())  #   Convertir a número decimal
                productos.append((producto, monto))
    return productos

#   Función principal que genera las boletas
def generar_boletas(productos, limite_por_boleta=700):
    """
    Agrupa productos en boletas sin superar el límite especificado.
    Si un producto excede individualmente el límite, se genera advertencia.
    """
    boletas = []
    boleta_actual = []
    total_actual = 0

    #   Procesar cada producto del documento
    for producto, monto in productos:
        #   Verificar si el producto cabe en la boleta actual
        if total_actual + monto <= limite_por_boleta:
            boleta_actual.append((producto, monto))
            total_actual += monto
        else:
            #   Guardar boleta actual si tiene productos
            if boleta_actual:
                boletas.append(boleta_actual)
                boleta_actual = []  #   Reiniciar boleta
                total_actual = 0
            
            #   Manejar productos que exceden individualmente el límite
            if monto > limite_por_boleta:
                print(f"¡Advertencia! El producto '{producto}' (S/{monto}) excede el límite por boleta.")
            
            #   Agregar producto a nueva boleta
            boleta_actual.append((producto, monto))
            total_actual += monto

    #   Asegurar que la última boleta se guarde
    if boleta_actual:
        boletas.append(boleta_actual)

    return boletas

#   Función para mostrar boletas en consola
def mostrar_boletas(boletas):
    """
    Muestra las boletas generadas con formato legible.
    Incluye número de boleta, productos y total.
    """
    for i, boleta in enumerate(boletas, 1):  #   Numerar desde 1
        print(f"\nBOLETA {i}")
        total_boleta = 0
        for producto, monto in boleta:
            print(f"Producto: {producto} = S/{monto:.2f}")  #   Formato 2 decimales
            total_boleta += monto
        print(f"Total Boleta {i}: S/{total_boleta:.2f}")

#   Función para guardar resultados en CSV
def guardar_boletas_csv(boletas, archivo_salida="boletas_generadas.csv"):
    """
    Exporta las boletas a un archivo CSV.
    Estructura: Boleta,Producto,Monto
    """
    #   Abrir archivo en modo escritura
    with open(archivo_salida, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        #   Escribir encabezado
        writer.writerow(["Boleta", "Producto", "Monto (S/)"])
        for i, boleta in enumerate(boletas, 1):
            for producto, monto in boleta:
                writer.writerow([f"Boleta {i}", producto, monto])

#   Bloque principal de ejecución
if __name__ == "__main__":
    #   Configuración inicial
    archivo_csv = "documento_interno.csv"  #   Nombre archivo de entrada
    limite_por_boleta = 700  #   Límite configurable

    try:
        #   Paso 1 - Leer archivo de entrada
        productos = leer_documento_interno(archivo_csv)
        if not productos:
            print("El archivo CSV está vacío o no tiene datos válidos.")
            exit()

        #   Paso 2 - Mostrar resumen del documento
        total_documento = sum(monto for _, monto in productos)
        print(f"\nDOCUMENTO INTERNO - Total: S/{total_documento:.2f}")
        for producto, monto in productos:
            print(f"{producto} = S/{monto:.2f}")

        #   Paso 3 - Generar boletas
        boletas_generadas = generar_boletas(productos, limite_por_boleta)
        print(f"\nSe generaron {len(boletas_generadas)} boleta(s):")
        mostrar_boletas(boletas_generadas)

        #   Paso 4 - Guardar resultados
        guardar_boletas_csv(boletas_generadas)
        print(f"\nResultados guardados en 'boletas_generadas.csv'")

    #   Manejo de errores comunes
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_csv}'")
    except ValueError:
        print("Error: Los montos deben ser números válidos (ejemplo: 500 o 250.50)")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")