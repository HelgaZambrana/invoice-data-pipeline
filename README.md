# Invoice Data Pipeline with FastAPI & Supabase

## 🚀 Project Overview

This project simulates a real-world data pipeline to process and ingest invoice data using:

- FastAPI for API development
- Pandas for data manipulation
- Supabase (PostgreSQL) as the database layer
- Docker for containerized deployment
- Pytest for integration tests

It supports both real insertions and dry_run (test mode) to ensure data is valid before touching production

---

## 🧠 Why This Project?

As a Data Analyst exploring the Data Engineering world, I wanted to build an end-to-end solution:

- Upload CSVs that are similar to those provided by users
- Validate required fields
- Clean & transform data (with full traceability)
- Insert into a real DB (hosted on Supabase)
- Offer preview / dry-run safety mode
- Be deployable in real scenarios via Docker

---

## 📁 Project Structure

```plaintext
invoice-data-pipeline/
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Config, logging, DB connection
│   ├── services/        # Ingestion, validation, transformation, loading
├── data/
│   ├── samples/         # Sample CSVs for testing
│   ├── logs/            # App + transformation logs
├── tests/               # Integration tests with dry_run and real insert
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
└── README.md            
```

---
## 📦 How to Run

### Locally (Dev)

uvicorn app.main:app --reload

Then go to http://localhost:8000/docs and use the Swagger UI.

### With Docker

docker-compose up --build

Then access: http://localhost:8000/docs

---

## 🧪 Run Tests

pytest tests/

Includes:
- File upload and DB verification
- Dry run integrity
- Log content assertions