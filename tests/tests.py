# Testing for Capstone Data Warehouse Project
# Author: Jarome Leslie
# Date: 2022-01-03

import os
import sys

import pytest
from airflow.models import DagBag

sys.path.append(os.path.join(os.path.dirname(__file__), "../dags"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../plugins"))

# Airflow variables called from DAGs under test are stubbed out
os.environ["AIRFLOW_VAR_DATA_LAKE_BUCKET"] = "test_bucket"
os.environ["AIRFLOW_VAR_ATHENA_QUERY_RESULTS"] = "SELECT 1;"
os.environ["AIRFLOW_VAR_SNS_TOPIC"] = "test_topic"
os.environ["AIRFLOW_VAR_REDSHIFT_UNLOAD_IAM_ROLE"] = "test_role_1"
os.environ["AIRFLOW_VAR_GLUE_CRAWLER_IAM_ROLE"] = "test_role_2"


@pytest.fixture(params=["../dags/"])
def dag_bag(request):
    return DagBag(dag_folder=request.param, include_examples=False)


def test_no_import_errors(dag_bag):
    assert not dag_bag.import_errors
