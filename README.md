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
