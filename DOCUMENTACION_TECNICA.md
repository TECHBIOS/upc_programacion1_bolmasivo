# Documentación Técnica - Sistema de Boletas Electrónicas

## 🏗️ Arquitectura del Sistema

### Estructura Modular

El sistema está diseñado con una arquitectura modular que separa las responsabilidades:

```
┌─────────────────┐    ┌───────────────────┐    ┌─────────────────┐
│   main.py       │    │ boleta_electronica│    │   config.py     │
│   (Entrada)     │◄──►│   .py             │◄──►│  (Configuración)│
│                 │    │   (Lógica)        │    │                 │
└─────────────────┘    └───────────────────┘    └─────────────────┘
                                 │                       │
                                 ▼                       ▼
                       ┌───────────────────┐    ┌─────────────────┐
                       │ ejemplo_Documentos│    │ requirements.txt│
                       │ Internos.xlsx     │    │  (Dependencias) │
                       └───────────────────┘    └─────────────────┘
```

### Componentes Principales

#### 1. `main.py` - Punto de Entrada
- **Responsabilidad**: Interfaz de usuario y orquestación
- **Funciones principales**:
  - `main()`: Función principal del programa
  - `mostrar_ayuda()`: Sistema de ayuda integrado
- **Características**:
  - Manejo de argumentos de línea de comandos
  - Validación de archivos de entrada
  - Presentación de resultados formateados

#### 2. `boleta_electronica.py` - Lógica de Negocio
- **Responsabilidad**: Procesamiento central del sistema
- **Clase principal**: `BoletaElectronica`
- **Métodos clave**:
  - `leer_archivo_entrada()`: Lectura y validación de datos Excel
  - `calcular_subtotal_item()`: Cálculos matemáticos
  - `dividir_item_grande()`: División de ítems que exceden límite
  - `optimizar_empaquetado()`: Algoritmo de optimización mejorado
  - `generar_boleta()`: Creación de boletas individuales
  - `procesar_documento()`: Procesamiento por documento
  - `generar_archivos_salida()`: Exportación de resultados en carpeta 'out/'

#### 3. `config.py` - Configuración
- **Responsabilidad**: Parámetros configurables del sistema
- **Configuraciones**:
  - `LIMITE_MAXIMO_BOLETA`: S/ 600 (configurable)
  - `PORCENTAJE_IGV`: 18% (configurable)
  - `DATOS_CLIENTE`: Información genérica del cliente
  - `SERIE_BOLETA`: Serie de numeración
  - `ARCHIVO_ENTRADA`: Nombre del archivo de entrada

## 🔧 Algoritmos Implementados

### 1. Algoritmo de División de Ítems Grandes

```python
def dividir_item_grande(self, item, limite):
    subtotal_item = cantidad * precio_unitario
    
    if subtotal_item <= limite:
        return [item]  # No necesita división
    
    # Calcular número de partes necesarias
    num_partes = int(subtotal_item / limite) + 1
    cantidad_por_parte = cantidad / num_partes
    
    # Crear partes divididas
    items_divididos = []
    for i in range(num_partes):
        item_dividido = item.copy()
        item_dividido['cantidad'] = cantidad_por_parte
        items_divididos.append(item_dividido)
    
    return items_divididos
```

**Complejidad**: O(n) donde n es el número de partes necesarias

### 2. Algoritmo de Optimización de Empaquetado

```python
def optimizar_empaquetado(self, items, limite):
    # 1. Dividir ítems grandes
    items_procesados = []
    for item in items:
        items_divididos = self.dividir_item_grande(item, limite)
        items_procesados.extend(items_divididos)
    
    # 2. Procesar por producto para optimizar llenado
    boletas = []
    boleta_actual = []
    subtotal_actual = 0.0
    
    # Agrupar por producto
    productos = {}
    for item in items_procesados:
        producto = item['descripcion']
        if producto not in productos:
            productos[producto] = []
        productos[producto].append(item)
    
    # Procesar cada producto
    for producto, items_producto in productos.items():
        for item in items_producto:
            if subtotal_actual + item['subtotal'] <= limite:
                boleta_actual.append(item)
                subtotal_actual += item['subtotal']
            else:
                if boleta_actual:
                    boletas.append(boleta_actual)
                boleta_actual = [item]
                subtotal_actual = item['subtotal']
    
    # Agregar última boleta si tiene items
    if boleta_actual:
        boletas.append(boleta_actual)
    
    return boletas
```

**Complejidad**: O(n log n) debido al procesamiento por producto
**Estrategia**: Algoritmo optimizado que procesa por producto para llenar boletas más eficientemente

## 📊 Estructura de Datos

### 1. Formato de Entrada (Excel - Tabla Plana)

```xlsx
SERIE;NUMERO;FECHA;CLIENTE;MONEDA;TOTAL;PRODUCTO;PRECIO;CANTIDAD;IMPORTE
B001;1;27/06/2025;Industrias SAC;Soles;900.00;Garbanzo;10.00;90.00;900.00
B001;1;27/06/2025;Industrias SAC;Soles;100.00;Arroz;10.00;10.00;100.00
```

### 2. Estructura de Ítem Interna

```python
item = {
    'codigo': 'ITEM001',
    'descripcion': 'Garbanzo',
    'cantidad': 90.0,
    'precio_unitario': 10.0,
    'subtotal': 900.0
}
```

### 3. Estructura de Boleta

```python
boleta = {
    'serie': 'B001',
    'numero': 'B001-000001',
    'fecha_emision': '2024-01-15',
    'cliente': {...},
    'items': [...],
    'subtotal': 600.0,
    'igv': 108.0,
    'total': 708.0,
    'documento_origen': 'D001-1'
}
```

## 🔍 Validaciones y Control de Errores

### 1. Validación de Archivo de Entrada

```python
def validar_archivo_entrada(archivo):
    # Verificar existencia
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {archivo}")
    
    # Verificar formato (solo Excel)
    if not archivo.endswith(('.xlsx', '.xls')):
        raise ValueError(f"Formato no soportado: {archivo}. Solo se aceptan archivos Excel")
    
    # Verificar columnas requeridas
    columnas_requeridas = ['SERIE', 'NUMERO', 'FECHA', 'CLIENTE', 'MONEDA', 
                          'TOTAL', 'PRODUCTO', 'PRECIO', 'CANTIDAD', 'IMPORTE']
    columnas_faltantes = set(columnas_requeridas) - set(df.columns)
    if columnas_faltantes:
        raise ValueError(f"Columnas faltantes: {columnas_faltantes}")
```

### 2. Validación de Datos

```python
def validar_datos(df):
    # Limpiar espacios en nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Verificar tipos de datos
    if not pd.api.types.is_numeric_dtype(df['CANTIDAD']):
        raise ValueError("Columna 'CANTIDAD' debe ser numérica")
    
    if not pd.api.types.is_numeric_dtype(df['PRECIO']):
        raise ValueError("Columna 'PRECIO' debe ser numérica")
    
    # Verificar valores positivos
    if (df['CANTIDAD'] <= 0).any():
        raise ValueError("Cantidades deben ser positivas")
    
    if (df['PRECIO'] <= 0).any():
        raise ValueError("Precios deben ser positivos")
```

### 3. Validación de Totales

```python
def validar_totales(original, generado):
    diferencia = abs(original - generado)
    if diferencia > 0.01:  # Tolerancia de 1 centavo
        raise ValueError(f"Totales no coinciden: {diferencia}")
```

## 📈 Análisis de Rendimiento

### 1. Complejidad Temporal

| Operación | Complejidad | Descripción |
|-----------|-------------|-------------|
| Lectura de archivo Excel | O(n) | n = número de registros |
| División de ítems | O(m) | m = número de ítems grandes |
| Optimización por producto | O(n log n) | Ordenamiento + empaquetado |
| Generación de boletas | O(k) | k = número de boletas |
| **Total** | **O(n log n)** | Dominado por optimización |

### 2. Complejidad Espacial

| Componente | Espacio | Descripción |
|------------|---------|-------------|
| DataFrame de entrada | O(n) | Datos originales |
| Items procesados | O(n) | Items después de división |
| Boletas generadas | O(k) | k = número de boletas |
| **Total** | **O(n + k)** | Lineal con el tamaño de entrada |

### 3. Casos de Uso Típicos

| Escenario | Documentos | Items | Boletas | Tiempo Estimado |
|-----------|------------|-------|---------|-----------------|
| Pequeño | 1-5 | 10-50 | 5-20 | < 1 segundo |
| Mediano | 10-50 | 100-500 | 50-200 | 1-5 segundos |
| Grande | 100+ | 1000+ | 500+ | 5-30 segundos |

## 🧪 Sistema de Pruebas

### 1. Pruebas Unitarias

```python
def test_calculo_subtotal():
    """Prueba el cálculo de subtotales"""
    sistema = BoletaElectronica()
    
    casos = [
        (2, 2500, 5000),  # Caso normal
        (0, 100, 0),      # Cantidad cero
        (1, 0, 0),        # Precio cero
    ]
    
    for cantidad, precio, esperado in casos:
        resultado = sistema.calcular_subtotal_item(cantidad, precio)
        assert abs(resultado - esperado) < 0.01
```

### 2. Pruebas de Integración

```python
def test_procesamiento_completo():
    """Prueba el flujo completo del sistema"""
    # Crear datos de prueba en formato Excel
    # Procesar con el sistema
    # Verificar resultados
    # Validar archivos de salida en carpeta 'out/'
```

### 3. Pruebas de Validación

```python
def test_validacion_totales():
    """Prueba que los totales coincidan"""
    # Comparar total original vs total boletas
    # Verificar que la diferencia sea < 0.01
```

## 🔧 Configuración y Personalización

### 1. Parámetros Configurables

```python
# En config.py
LIMITE_MAXIMO_BOLETA = 600.00  # Límite por boleta (actualizado)
PORCENTAJE_IGV = 18.0          # Porcentaje de IGV
SERIE_BOLETA = "B001"          # Serie de numeración
NUMERO_INICIAL = 1             # Número inicial
```

### 2. Datos del Cliente

```python
DATOS_CLIENTE = {
    "nombre": "CLIENTE VARIOS",
    "tipo_documento": "DNI",
    "numero_documento": "00000000",
    "direccion": "DIRECCIÓN GENÉRICA"
}
```

### 3. Formato de Archivos

```python
ARCHIVO_ENTRADA = "DocumentosInternos.xlsx"  # Solo archivos Excel
ARCHIVO_LOG = "log_procesamiento.txt"
# Los archivos de salida se generan dinámicamente en carpeta 'out/'
```

## 📤 Formato de Salida (Archivos en carpeta 'out/')

### Estructura de archivos de salida:
```
out/
├── boletas_[SERIE]_[NUMERO].xlsx    # Boletas en Excel
├── boletas_[SERIE]_[NUMERO].json    # Datos en JSON
└── log_procesamiento.txt            # Log del procesamiento
```

### Formato del archivo Excel:
El archivo Excel contiene las boletas generadas en el siguiente formato:

| SERIE-NUMERO | FECHA | CLIENTE | MONEDA | SUBTOTAL | IGV | TOTAL | ANEXO | PRODUCTO | PRECIO | CANTIDAD | IMPORTE |
|--------------|-------|---------|--------|----------|-----|-------|-------|----------|--------|----------|---------|
| B001-1       | 27/06/2025 | Cliente varios | Soles | 600.00 | 108.00 | 708.00 | D001-1 | Garbanzo | 10.00 | 60.00 | 600.00 |
| B001-2       | 27/06/2025 | Cliente varios | Soles | 300.00 | 54.00 | 354.00 | D001-1 | Garbanzo | 10.00 | 30.00 | 300.00 |

**Descripción de columnas**:
- **SERIE-NUMERO**: Número de la boleta generada
- **FECHA**: Fecha de emisión de la boleta
- **CLIENTE**: Nombre del cliente
- **MONEDA**: Moneda utilizada (ej. Soles)
- **SUBTOTAL**: Subtotal de la boleta (sin IGV)
- **IGV**: Monto del Impuesto General a las Ventas (18%)
- **TOTAL**: Total de la boleta (subtotal + IGV)
- **ANEXO**: Documento de origen (referencia interna)
- **PRODUCTO**: Descripción del producto
- **PRECIO**: Precio unitario del producto
- **CANTIDAD**: Cantidad de producto en la boleta
- **IMPORTE**: Subtotal del producto en la boleta

### Formato del archivo JSON:
```json
{
  "boletas": [...],
  "documento": "D001-1",
  "resumen": {
    "total_boletas": 3,
    "fecha_procesamiento": "2024-01-15T10:30:00"
  }
}
```

## 📝 Logging y Monitoreo

### 1. Configuración de Logging

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ARCHIVO_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

### 2. Eventos Registrados

- ✅ Lectura de archivos Excel
- 📊 Análisis de datos
- 🔄 Procesamiento de documentos
- 🧾 Generación de boletas
- 📁 Creación de archivos de salida
- ⚠️ Advertencias y errores
- 📈 Estadísticas finales

## 🚀 Optimizaciones Implementadas

### 1. Algoritmo Optimizado para Empaquetado

- Procesa ítems por producto
- Llena boletas lo más cerca posible al límite configurado
- Minimiza el número total de boletas generadas

### 2. División Inteligente de Ítems

- Solo divide ítems que exceden el límite de S/ 600
- Mantiene proporciones exactas
- Evita divisiones innecesarias

### 3. Procesamiento por Lotes

- Procesa múltiples documentos
- Mantiene trazabilidad por documento
- Optimiza uso de memoria

### 4. Generación de Archivos Organizada

- Archivos de salida en carpeta 'out/'
- Nombres descriptivos con serie y número del documento
- Separación por documento interno

## 🔒 Consideraciones de Seguridad

### 1. Validación de Entrada

- Verificación de tipos de datos
- Validación de rangos
- Sanitización de strings
- Limpieza de espacios en nombres de columnas

### 2. Manejo de Errores

- Excepciones específicas
- Mensajes informativos
- Recuperación graceful
- Conversión de tipos numpy para JSON

### 3. Logging Seguro

- No registra datos sensibles
- Información de auditoría
- Trazabilidad completa

## 📚 Referencias y Estándares

### 1. Estándares de Programación

- PEP 8: Guía de estilo de Python
- PEP 257: Docstrings
- Type hints para mejor documentación

### 2. Librerías Utilizadas

- **pandas**: Manipulación de datos tabulares
- **openpyxl**: Lectura de archivos Excel
- **numpy**: Operaciones numéricas
- **logging**: Sistema de logs estándar

### 3. Formatos de Archivo

- **Excel**: Formato estándar de Microsoft (.xlsx)
- **JSON**: RFC 7159
- **CSV**: Ya no se utiliza

## 🔄 Flujo de Procesamiento

### 1. Lectura de Datos
1. Validar existencia del archivo Excel
2. Leer datos con pandas
3. Validar estructura de columnas
4. Limpiar espacios en nombres de columnas

### 2. Procesamiento
1. Agrupar por documento interno
2. Procesar cada documento por separado
3. Optimizar empaquetado por producto
4. Generar boletas individuales

### 3. Generación de Salida
1. Crear carpeta 'out/' si no existe
2. Generar archivos Excel por documento
3. Generar archivos JSON por documento
4. Registrar logs del proceso

---

**Nota**: Esta documentación técnica está diseñada para desarrolladores que necesiten entender, mantener o extender el sistema de boletas electrónicas. El sistema ha sido optimizado para trabajar exclusivamente con archivos Excel y generar salidas organizadas en la carpeta 'out/' con nombres descriptivos. 