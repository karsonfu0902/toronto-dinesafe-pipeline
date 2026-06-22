import os
from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

profile_config = ProfileConfig(
    profile_name='default',
    target_name='dev',
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id='snowflake_conn',
        profile_args={'database':'analytics_zone_db', 'schema':'dinesafe_marts'}
    )
)

dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig('/usr/local/airflow/dags/dbt/data_pipeline'),
    operator_args={'install_deps':True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path="/usr/local/airflow/dbt_venv/bin/dbt"),
    schedule='@daily',
    start_date=datetime(2026, 3, 25),
    catchup=False,
    dag_id='dbt_dag'
)