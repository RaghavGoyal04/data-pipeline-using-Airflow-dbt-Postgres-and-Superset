# Weather Data Dashboard

A modern data pipeline for ingesting, transforming, and visualizing weather data using **Airflow**, **DBT**, **PostgreSQL**, and **Superset**.

---

## Tech Stack

- **Apache Airflow**: Orchestrates the data pipeline.
- **DBT (Data Build Tool)**: Handles data transformation and modeling.
- **PostgreSQL**: Stores raw and transformed weather data.
- **Superset**: Provides interactive dashboards and data visualization.
- **Docker**: Containerizes services for easy setup and reproducibility.
- **Python**: Main programming language for ETL and orchestration.

---

## Project Structure

```
weather-dashboard/
│
├── airflow/
│   └── dags/
│       ├── orchestrator.py         # Main Airflow DAG for the pipeline
│       ├── dbt_orchestrator.py     # DBT orchestration DAG
│
├── dbt/
│   ├── dbt_project/                # DBT project directory
│   └── profiles.yml                # DBT profiles configuration
│
├── .env                            # Environment variables (DB credentials, etc.)
├── docker-compose.yaml             # Docker Compose setup for services
└── ...
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd weather-dashboard
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with your database and API credentials:

```
POSTGRES_DB=weather_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
# Add other variables as needed
```

### 3. Start Services with Docker Compose

```bash
docker-compose up --build
```

This will launch:
- Airflow (webserver, scheduler)
- PostgreSQL
- Superset
- Any other defined services

### 4. Initialize Airflow

If running Airflow for the first time:

```bash
docker exec -it <airflow_container_name> airflow db init
docker exec -it <airflow_container_name> airflow users create \
    --username admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

### 5. Set Up DBT

Install dependencies and run DBT models:

```bash
cd dbt/dbt_project
dbt deps
dbt run
```

### 6. Access the Services

- **Airflow UI:** http://localhost:8080
- **Superset UI:** http://localhost:8088
- **PostgreSQL:** Connect using credentials from `.env`

---

## Usage

- The Airflow DAG (`orchestrator.py`) fetches weather data, loads it into PostgreSQL, and triggers DBT for transformation.
- Superset connects to PostgreSQL for dashboarding and analytics.

---

## Notes

- Make sure your `.env` file is up to date and contains all required variables.
- You may need to adjust file paths in Airflow DAGs if running outside Docker.
- For local development, ensure Python dependencies are installed (`pip install -r requirements.txt`).

---

## Author

Raghav Goyal
