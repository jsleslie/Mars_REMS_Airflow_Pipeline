from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

# import download_REMS_s3
# import download_Ozone_s3
import boto3
from operators import (
    StageToRedshiftOperator,
    LoadFactOperator,
    LoadDimensionOperator,
    DataQualityOperator,
)
from helpers import SqlQueries, download_REMS_s3

#
# The following DAG performs the following functions:
#
#       1. Uploads Mars data from local system to S3
#       2. Stages data from S3 into Redshift
#       3. Performs a data quality check on the REMS and Ozone tables in Redshift
#       4. Uses the FactsCalculatorOperator to create a Facts table in Redshift
#           a. **NOTE**: to complete this step you must complete the FactsCalcuatorOperator
#              skeleton defined in plugins/operators/facts_calculator.py
#

default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 12, 7),
    "retries": 1,
    "retries_delay": timedelta(seconds=10),
}

with DAG(
    "Mars_DWH_Capstone",
    default_args=default_args,
    schedule_interval="@monthly",
    catchup=False,
) as dag:

    def printString():
        print("This is a Test String")

    start_operator = DummyOperator(task_id="Begin_execution")

    download_REMS_to_s3 = PythonOperator(
        task_id="download_REMS_to_S3", python_callable=download_REMS_s3.main
    )

    create_tables = PostgresOperator(
        task_id="Initialize_tables",
        postgres_conn_id="redshift",
        sql=SqlQueries.create_tables,
    )

    stage_REMS_ENV_redshift = StageToRedshiftOperator(
        task_id="Stage_REMS_ENV_Redshift",
        table="stg_REMS_ENV",
        s3_bucket="jsleslie-data-engineering-capstone-1.0",
        s3_key="REMS_ENV/",
    )

    stage_REMS_ADR_redshift = StageToRedshiftOperator(
        task_id="Stage_REMS_ADR_Redshift",
        table="stg_REMS_ADR",
        s3_bucket="jsleslie-data-engineering-capstone-1.0",
        s3_key="REMS_ADR/",
    )

    load_measures_table = LoadFactOperator(
        task_id="Load_measures_fact_table",
        table="measures",
        sql=SqlQueries.measures_table_insert,
    )

    load_location_table = LoadDimensionOperator(
        task_id="Load_location_dimension_table",
        table="location",
        sql=SqlQueries.location_table_insert,
    )

    load_time_table = LoadDimensionOperator(
        task_id="Load_time_dimension_table",
        table="time",
        sql=SqlQueries.time_table_insert,
    )

    run_quality_checks = DataQualityOperator(
        task_id="Run_data_quality_checks",
        dq_checks=[
            {
                "check_sql": "SELECT COUNT(*) FROM measures WHERE measure_id is null",
                "expected_result": 0,
            },
            {
                "check_sql": "SELECT COUNT(*) FROM time WHERE  time_id is null",
                "expected_result": 0,
            },
            {
                "check_sql": "SELECT COUNT(*) FROM location WHERE  location_id is null",
                "expected_result": 0,
            },
        ],
    )

    end_operator = DummyOperator(task_id="Stop_execution")

    # # Create dependency logic
    start_operator >> create_tables
    create_tables >> download_REMS_to_s3
    download_REMS_to_s3 >> stage_REMS_ENV_redshift
    download_REMS_to_s3 >> stage_REMS_ADR_redshift
    stage_REMS_ENV_redshift >> load_measures_table
    stage_REMS_ADR_redshift >> load_measures_table
    stage_REMS_ADR_redshift >> load_location_table
    stage_REMS_ENV_redshift >> load_time_table
    stage_REMS_ADR_redshift >> load_time_table
    load_measures_table >> run_quality_checks
    load_location_table >> run_quality_checks
    load_time_table >> run_quality_checks
    run_quality_checks >> end_operator
