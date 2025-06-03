# 🧾 Invoice ETL Pipeline

Este proyecto simula un pipeline real de carga de facturas desde múltiples distribuidores. Modulariza el flujo en etapas independientes: lectura, transformación, validación y carga. Cada parte está desacoplada para permitir testing, mantenimiento y escalabilidad. La base de datos es un PostgreSQL gestionado por Supabase y el backend está desarrollado con FastAPI.

---

## 🚀 Tecnologías utilizadas

- Python
- FastAPI
- Pandas
- PostgreSQL / Supabase
- Docker
- Pytest (para testing)
- dotenv

---

## 📁 Estructura del proyecto

```plaintext
invoice-data-pipeline/
├── app/
│ ├── api/ # Endpoints FastAPI
│ ├── core/ # Configuración (env, logger)
│ ├── services/ # Ingestión, validación, transformación, carga
│ └── main.py # Entrada principal
├── data/samples/ # Archivos de prueba (.csv, .xlsx)
├── db/ # SQL para creación de tablas
├── tests/ # Tests automatizados con pytest
├── .env # Variables de entorno (no versionado)
├── requirements.txt # Dependencias
└── README.md                 
```

---

## 💡 Use Case: Procesamiento de facturas mensuales

Un Data Analyst recibe facturas mensuales en distintos formatos (.csv, .xls, .xlsx). Utiliza esta API para:

1. Subir el archivo al endpoint `/upload`.
2. Validar automáticamente que las columnas requeridas estén presentes (`product`, `price`, `quantity`, `customer`).
3. Ver una vista previa de los datos.
4. Cargar los datos directamente en una base PostgreSQL (ejemplo: Supabase), donde el equipo de BI puede consultarlos.

Esta automatización ahorra tiempo, reduce errores manuales y estandariza el flujo de datos entrantes.

📌 Resultado esperado:
```json
{
  "filename": "invoice_demo.csv",
  "rows_inserted": 3,
  "columns": ["product", "price", "quantity", "customer"],
  "preview": [
    {"product": "Mouse", "price": 20.5, "quantity": 2, "customer": "Juan Perez"},
    ...
  ]
}
```

---

## ✅ Testing
Este proyecto incluye tests automatizados para los módulos principales (validator, ingestion).

- validator.py	Verifica si un archivo contiene las columnas requeridas
- ingestion.py	Valida que un archivo .csv o .xlsx pueda convertirse correctamente en un DataFrame

Los archivos de prueba se encuentran en data/samples/:

- ✅ invoice_demo.csv → válido
- ✅ invoice_demo.xlsx → válido
- ❌ invoice_invalid.csv → faltan columnas
- ❌ invalid_file.txt → tipo no soportado
