# Municipal Health Inspection ELT Pipeline & Geo-Spatial Dashboard

An end-to-end data product that automates the ingestion, transformation, data quality testing, and geo-spatial profiling of municipal restaurant safety inspection logs. 

## Architecture Overview
* **Orchestration & Containerization:** Apache Airflow (via Astronomer Astro CLI) running in Docker to manage pipeline dependency chains.
* **Data Warehouse:** Snowflake (Targeted database: `analytics_zone_db`).
* **Transformation & Modeling:** dbt Core executing modular SQL statements to construct a resilient Star Schema.
* **Data Quality Framework:** Upstream schema assertions (uniqueness, nullability, and referential integrity) evaluated via dbt test layers.
* **Analytics Frontend:** Python-based Streamlit application rendering an algorithmic, severity-weighted Pydeck `HeatmapLayer`.

---

## Repository Structure

```text
toronto-dinesafe-pipeline/
├── dbt-dag/                   # Backend Airflow Orchestration & Environment
│   ├── dags/
│   │   ├── dbt_dag.py         # Cosmos DAG definition
│   │   └── dbt/
│   │       └── data_pipeline/ # dbt Core project (Models, seeds, schema tests)
│   └── Dockerfile             # Custom container setup with isolated dbt venv
│
├── dinesafe-map/              # Frontend Streamlit Visualization Application
│   └── streamlit_app.py       # Pydeck geo-spatial density application
│
└── scripts/                   # Snowflake Initialization
    └── dinesafe_snowflake_dbt_airflow_proj.sql
