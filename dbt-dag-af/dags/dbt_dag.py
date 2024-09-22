import os
from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping


profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_conn", 
        profile_args={"database": "db_dbt_elt", "schema": "schema_dbt_elt"},
    )
)
DBT_PROJECT_DIR = "/home/prashant-newway/Documents/DataEngineering/de2-dbt-elt/dbt-dag-af/include/dbt_elt_pipeline"
#DBT_PROFILES_DIR = "home/prashant-newway/Documents/DataEngineering/de2-dbt-elt/dbt-dag-af/include/"

dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig(DBT_PROJECT_DIR,),
    #profile_config=ProfileConfig(profiles_dir=DBT_PROFILES_DIR),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/.venv-dbt-af/bin/dbt",),
    schedule_interval="@daily",
    start_date=datetime(2024, 9, 20),
    catchup=False,
    dag_id="dbt_elt_sf__af_dag",
)

