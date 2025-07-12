# Sistema de Emisión Masiva de Boletas Electrónicas

## 📋 Descripción

Sistema automatizado en Python 3 para la emisión masiva de boletas electrónicas a partir de documentos internos. El sistema lee archivos Excel con documentos internos y genera boletas optimizadas respetando el límite máximo de S/ 699 por boleta.

## 🚀 Características

- **Lectura de archivos**: Soporte para archivos Excel (.xlsx, .xls)
- **Optimización automática**: Divide ítems grandes y optimiza el empaquetado para minimizar el número de boletas
- **Cálculo automático**: IGV (18%) y totales calculados automáticamente
- **Formatos de salida**: Excel y JSON con todos los detalles
- **Logging completo**: Registro detallado de todo el proceso
- **Validación de datos**: Verificación de totales y consistencia
- **Procesamiento por lotes**: Manejo de múltiples documentos internos
- **Organización de salida**: Archivos organizados en carpeta "out" con nombres descriptivos

## 📁 Estructura del Proyecto

```
upc_programacion1_bolmasivo/
├── main.py                      # Programa principal
├── boleta_electronica.py       # Clase principal del sistema
├── config.py                   # Configuración del sistema
├── requirements.txt            # Dependencias
├── .gitignore                  # Archivos a ignorar en Git
├── ejemplo_DocumentosInternos.xlsx  # Archivo de ejemplo
├── DOCUMENTACION_TECNICA.md    # Documentación técnica
├── out/                        # Carpeta de archivos de salida
│   ├── boletas_D001-1.xlsx     # Boletas generadas para D001-1
│   ├── boletas_D001-1.json     # Datos JSON para D001-1
│   └── ...                     # Más archivos según documentos procesados
├── log_procesamiento.txt       # Log del procesamiento
└── README.md                   # Este archivo
```

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd upc_programacion1_bolmasivo
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Formato del Archivo de Entrada

El archivo debe llamarse `DocumentosInternos.xlsx` y **OBLIGATORIAMENTE** seguir el nuevo formato estructurado:

### Estructura Requerida:
```xlsx
SERIE;NUMERO;FECHA;CLIENTE;MONEDA;TOTAL;PRODUCTO;PRECIO;CANTIDAD;IMPORTE
[Serie];[Numero];[Fecha];[Cliente];[Moneda];[Total];[Producto];[Precio];[Cantidad];[Importe]
```

### Ejemplo de archivo de entrada:

| SERIE | NUMERO | FECHA | CLIENTE | MONEDA | TOTAL | PRODUCTO | PRECIO | CANTIDAD | IMPORTE |
|--------------|-------|---------|--------|-------|-------|----------|--------|----------|---------|
| B001  | 1 | 27/06/2025 | Industrias SAC | Soles | 900.00 | Garbanzo | 10.00 | 90.00 | 900.00 |
| B001  | 1 | 27/06/2025 | Industrias SAC | Soles | 100.00 | aRROZ | 10.00 | 10.00 | 100.00 |

**⚠️ IMPORTANTE**: El sistema **SOLO acepta** este formato. Cualquier otro formato será rechazado y la ejecución se cancelará.

## 🎯 Uso del Sistema

### Ejecución básica:
```bash
python main.py
```

### Ver ayuda:
```bash
python main.py --help
```

## 📤 Archivos de Salida

El sistema genera los archivos de salida en la carpeta `out/` con nombres que incluyen la serie y número del documento interno:

### Estructura de archivos de salida:
```
out/
├── boletas_[SERIE-NUMERO].xlsx    # Boletas en Excel
├── boletas_[SERIE-NUMERO].json    # Datos en JSON
└── log_procesamiento.txt          # Log del procesamiento
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
El archivo JSON contiene todos los datos estructurados de las boletas generadas, incluyendo:
- Información del documento interno
- Detalle de cada boleta
- Productos y cantidades
- Cálculos de IGV y totales

## ⚙️ Configuración

Edita el archivo `config.py` para modificar:

- **Límite máximo por boleta**: Actualmente S/ 699
- **Porcentaje IGV**: Actualmente 18%
- **Datos del cliente**: Información genérica del cliente
- **Serie de boletas**: Actualmente "B001"
- **Archivos de entrada/salida**: Nombres de archivos

## 🔧 Lógica de Negocio

### Procesamiento de ítems:
1. **Lectura**: Se lee el archivo de entrada y se validan las columnas
2. **Cálculo**: Se calcula el subtotal por ítem (cantidad × precio_unitario)
3. **División**: Si un ítem excede S/ 699, se divide en partes proporcionales
4. **Optimización**: Se empaquetan los ítems para minimizar el número de boletas
5. **Generación**: Se crean las boletas con IGV y totales calculados

### Algoritmo de optimización mejorado:
- Los ítems se procesan por producto
- Para cada producto, se reparte la cantidad en boletas llenas hasta el límite
- Se llenan las boletas lo más cerca posible al límite configurado
- Se minimiza el número total de boletas generadas

**Cobertura de pruebas**:
- ✅ Lectura de archivos Excel
- ✅ Cálculo de subtotales
- ✅ División de ítems grandes
- ✅ Optimización de empaquetado
- ✅ Procesamiento completo
- ✅ Validación de totales
- ✅ Generación de archivos de salida
- ✅ Manejo de errores

## 📈 Ejemplo de Resultado

**Entrada**: Documento interno D001-1 de S/ 5000 con 3 ítems
- 2 Laptops HP (S/ 2500 c/u) = S/ 5000
- 10 Mouses (S/ 50 c/u) = S/ 500  
- 5 Teclados (S/ 100 c/u) = S/ 500

**Salida**: Archivos en `out/boletas_D001-1.xlsx` y `out/boletas_D001-1.json`
- Boleta 1: 1 Laptop HP + 3 Mouses + 2 Teclados = S/ 2650 + S/ 477 IGV = S/ 3127
- Boleta 2: 1 Laptop HP + 3 Mouses + 2 Teclados = S/ 2650 + S/ 477 IGV = S/ 3127
- Boleta 3: 4 Mouses + 1 Teclado = S/ 300 + S/ 54 IGV = S/ 354
- ... (5 boletas más)

## 🔍 Validaciones

- ✅ Verificación de columnas requeridas
- ✅ Validación de totales (original vs boletas generadas)
- ✅ Control de límites por boleta
- ✅ Logging de errores y advertencias
- ✅ Manejo de excepciones
- ✅ Limpieza de espacios en nombres de columnas
- ✅ Conversión de tipos de datos para JSON

## 📚 Documentación Adicional

- **`DOCUMENTACION_TECNICA.md`**: Documentación técnica completa del sistema

## 🛡️ Control de Versiones

El proyecto incluye:
- Repositorio Git inicializado
- `.gitignore` configurado para Python
- Archivos de ejemplo incluidos
- Documentación completa

## 📝 Logs y Monitoreo

El sistema genera logs detallados que incluyen:
- Información de archivos procesados
- Número de boletas generadas por documento
- Errores y advertencias
- Tiempo de procesamiento
- Validaciones realizadas
- Ubicación de archivos de salida generados

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza los cambios
4. Ejecuta las pruebas
5. Envía un pull request

## 📄 Licencia

Este proyecto es parte del curso de Fundamentos de Programación de la UPC.

## 👨‍💻 Autor

Desarrollado para el curso de Fundamentos de Programación - UPC

---

**Nota**: Este sistema está diseñado para cumplir con los requisitos específicos de emisión de boletas electrónicas en Perú, respetando el límite máximo de S/ 600 por boleta según la normativa vigente. Los archivos de salida se organizan automáticamente en la carpeta `out/` con nombres descriptivos que incluyen la serie y número del documento interno procesado.
