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
invoice-etl-pipeline/
├── app/
│   ├── api/
│   ├── core/
│   ├── services/
│   └── main.py
├── data/
├── db/
├── tests/
├── venv/
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
