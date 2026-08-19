from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

import sys

sys.path.append("/opt/airflow/scripts")

from extract_api import extract_data
from upload_s3 import upload_to_s3
from glue_crawler import run_glue_crawler
from alerts import notify_failure


# =========================================================
# CONFIGURACIÓN GENERAL DAG
# =========================================================

default_args = {

    "owner": "Fernando",

    "start_date": datetime(2026,1,1),

    # Reintentos automáticos
    "retries": 3,

    "retry_delay": timedelta(
        minutes=5
    ),

    # Alertas Discord
    "on_failure_callback":notify_failure
}

# =========================================================
# FUNCIÓN INTERMEDIA PARA XCOM
# =========================================================

def upload_task_function(ti):

    # -----------------------------------------------------
    # Obtener valor retornado por extract_task
    # -----------------------------------------------------

    file_path = ti.xcom_pull(
        task_ids="extract_api_data"
    )

    # -----------------------------------------------------
    # Ejecutar subida S3 usando path dinámico
    # -----------------------------------------------------

    upload_to_s3(file_path)

# =========================================================
# DEFINICIÓN DAG
# =========================================================

with DAG(

    dag_id="retail_analytics_pipeline",

    default_args=default_args,

    schedule="@daily",

    catchup=False,

    description="Pipeline ETL con Airflow, Spark, S3, Data Quality y Glue Catalog"

) as dag:

    # =====================================================
    # START
    # =====================================================

    start = EmptyOperator(
        task_id="start"
    )

    # =====================================================
    # EXTRACCIÓN API
    # =====================================================

    extract_task = PythonOperator(

        task_id="extract_api_data",

        python_callable=extract_data
    )

    # =====================================================
    # UPLOAD S3
    # =====================================================

    upload_task = PythonOperator(

        task_id="upload_raw_s3",

        python_callable=upload_task_function
    )

    # =====================================================
    # SPARK ETL
    # =====================================================

    spark_task = BashOperator(

        task_id="run_spark_etl",

        bash_command="""
        spark-submit \
        --conf spark.executorEnv.AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --conf spark.executorEnv.AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        --conf spark.driverEnv.AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --conf spark.driverEnv.AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        /opt/airflow/spark_jobs/process_orders.py
        """
    )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    quality_task = BashOperator(

        task_id="run_data_quality",

        bash_command="""
        spark-submit \
        --conf spark.executorEnv.AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --conf spark.executorEnv.AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        --conf spark.driverEnv.AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --conf spark.driverEnv.AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        /opt/airflow/spark_jobs/data_quality.py
        """
    )

    # =====================================================
    # GLUE CRAWLER
    # =====================================================

    glue_task = PythonOperator(

        task_id="run_glue_crawler",

        python_callable=run_glue_crawler
    )

    # =====================================================
    # END
    # =====================================================

    end = EmptyOperator(

        task_id="end"
    )

    # =====================================================
    # DEPENDENCIAS
    # =====================================================

    start >> extract_task >> upload_task >> spark_task >> quality_task >> glue_task >> end





















# =========================================================
# DEFINICIÓN DAG
# =========================================================
with DAG(

    dag_id="ecommerce_pipeline",

    default_args=default_args,

    schedule="@daily",

    catchup=False

) as dag:

    # =====================================================
    # START
    # =====================================================

    start = EmptyOperator(
        task_id="start"
    )

    # =====================================================
    # EXTRAER API
    # =====================================================

    extract_task = PythonOperator(

        task_id="extract_api_data",

        python_callable=extract_data
    )

    # =====================================================
    # SUBIR S3
    # =====================================================

    upload_task = PythonOperator(

        task_id="upload_raw_s3",

        python_callable=upload_task_function
    )

    # =====================================================
    # SPARK JOB
    # =====================================================

    spark_task = BashOperator(

        task_id="run_spark_job",

        bash_command="""
        spark-submit \
        --conf spark.executorEnv.AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --conf spark.executorEnv.AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        --conf spark.driverEnv.AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --conf spark.driverEnv.AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        /opt/airflow/spark_jobs/process_orders.py
        """
    )

    # =====================================================
    # END
    # =====================================================

    end = EmptyOperator(
        task_id="end"
    )

    # =====================================================
    # DEPENDENCIAS
    # =====================================================

    start >> extract_task >> upload_task >> spark_task >> end
