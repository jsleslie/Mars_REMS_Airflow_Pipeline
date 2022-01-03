# Mars_REMS_Airflow_Pipeline
Udacity Data Engineering Capstone Project on the ETL of the Mars Curiosity Rover environmental data into S3 then a Redshift datawarehouse

![DAG Testing workflow](https://github.com/jsleslie/Mars_REMS_Airflow_Pipeline/actions/workflows/test_dags.yml/badge.svg)

![S3 Sync workflow](https://github.com/jsleslie/Mars_REMS_Airflow_Pipeline/actions/workflows/sync_dags.yml/badge.svg)


## Project Summary
This project combines multiple data sets on Mars observations and modelled weather data and organises it into an Amazon Redshift data lake. As part of this work, the data will be uploaded to S3 after which the data will be read from S3, processed using Spark and loaded back into S3 as a set of fact and dimensional tables.

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up