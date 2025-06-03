# 🧾 Invoice ETL Pipeline

Proyecto de Data Engineering que permite la carga, transformación y almacenamiento de archivos de facturas provenientes de múltiples distribuidores. Utiliza Python (Pandas), FastAPI, PostgreSQL (via Supabase) y Docker.

---

## 🚀 Funcionalidades

- Subida de archivos de facturas (`.csv`, `.xls`, `.xlsx`)
- Estandarización y transformación de datos con Pandas
- Carga a base de datos PostgreSQL (Supabase o local)
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
├── app/                          # Código principal de la app
│   ├── api/                      # Endpoints de FastAPI
│   │   └── routes.py             # Rutas principales (upload, trigger ETL)
│   ├── core/                     # Configuración y utilidades
│   │   ├── config.py             # Config de entorno (Supabase, etc.)
│   │   └── logger.py             # Logger centralizado
│   ├── services/                 # Lógica de negocio y procesamiento
│   │   ├── ingestion.py          # Ingesta de archivos (PENDIENTE)
│   │   ├── transformer.py        # Transformaciones con Pandas (PENDIENTE)
│   │   ├── loader.py             # Carga a la base de datos (PENDIENTE)
│   │   └── validator.py          # Validación de columnas (IMPLEMENTADO)
│   └── main.py                   # Punto de entrada de la app FastAPI
│
├── data/                         # Datos de ejemplo
│   └── samples/                  # Facturas .csv, .xlsx, etc. para pruebas
│
├── db/                           # Scripts SQL (creación de tablas)
│   └── schema.sql                # Definición inicial de `facturas`, etc.
│
├── tests/                        # Tests automatizados (pytest)
│   ├── test_transformer.py       # (PENDIENTE)
│   └── test_validator.py         # (Tests para validator.py)
│
├── .env                          # Variables de entorno (base de datos)
├── .gitignore                    # Ignorar `.env`, `venv/`, etc.
├── Dockerfile                    # Imagen para correr la app
├── docker-compose.yml            # Compose para FastAPI + PostgreSQL
├── requirements.txt              # Paquetes instalados
└── README.md                     # Descripción general del proyecto
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