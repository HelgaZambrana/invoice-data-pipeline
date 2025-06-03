# 🧾 Invoice ETL Pipeline

Este proyecto simula un pipeline real de carga de facturas desde múltiples distribuidores. Modulariza el flujo en etapas independientes: lectura, transformación, validación y carga. Cada parte está desacoplada para permitir testing, mantenimiento y escalabilidad. La base de datos es un PostgreSQL gestionado por Supabase y el backend está desarrollado con FastAPI.

---

## 🚀 Funcionalidades

- Subida de archivos de facturas (`.csv`, `.xls`, `.xlsx`)
- Estandarización y transformación de datos con Pandas
- Carga a base de datos PostgreSQL (Supabase)
- API REST con FastAPI para gestionar la ingesta y monitoreo
- Contenerización con Docker para facilitar despliegue

---

## 🧱 Tecnologías utilizadas

- Pandas
- FastAPI
- PostgreSQL (via Supabase)
- Docker
- Uvicorn

---

## 📁 Estructura del proyecto

```plaintext
invoice-data-pipeline/
│
├── app/                          
│   ├── api/                      
│   │   └── routes.py             # Definir el endpoint /upload y orquestar todo el pipeline
│   ├── core/                    
│   │   ├── config.py             # Centralizar las variables de entorno (.env) para DB, etc.
│   │   └── logger.py             # Definir un logger para mensajes de debug o errores
│   ├── services/                 
│   │   ├── ingestion.py          # Leer el archivo subido (UploadFile) y convertirlo en DataFrame
│   │   ├── transformer.py        # Limpiar y normalizar los nombres de columnas del DataFrame
│   │   ├── loader.py             # Conectar con Supabase y guardar los datos en la base de datos PostgreSQL
│   │   └── validator.py          # Verificar que estén las columnas mínimas requeridas
│   └── main.py                   # Punto de entrada de la app FastAPI
│
├── data/                        
│   └── samples/                  # Facturas .csv, .xlsx, etc. para pruebas
│
├── db/                          
│   └── schema.sql                # Definición inicial de `invoices`
│
├── tests/                        
│   ├── test_transformer.py       # (PENDIENTE)
│   └── test_validator.py         # (PENDIENTE)
│
├── .env                          
├── .gitignore                    
├── Dockerfile                    # Imagen para correr la app (PENDIENTE)
├── docker-compose.yml            # Compose para FastAPI + PostgreSQL (PENDIENTE)
├── requirements.txt              
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