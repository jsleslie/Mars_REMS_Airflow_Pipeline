# Mars Environment Redshift Data Warehouse & Airflow Pipeline
Udacity Data Engineering Capstone Project

![DAG Testing workflow](https://github.com/jsleslie/Mars_REMS_Airflow_Pipeline/actions/workflows/test_dags.yml/badge.svg)

![S3 Sync workflow](https://github.com/jsleslie/Mars_REMS_Airflow_Pipeline/actions/workflows/sync_dags.yml/badge.svg)


## Project Summary
This project combines multiple data sets on Mars observations and modelled weather data and organises it into an Amazon Redshift data warehouse via an Apache Airflow managed data pipeline. As part of this work, the data will be uploaded to S3 after which the data will be read from S3, then loading into staging tables in Redshift before the creation of fact and dimension tables. An overview of the ETL pipeline is provided in the Directed Acyclic Graph (DAG) below:

![capstone_dag](img/capstone_dag.png)

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up



## Project Scope and Data Sources



## References

- [Jet Propulsion Laboratory. Mars Science Laboratory (MSL) Software Interface Specification (SIS) Rover Environmental Monitoring Station (REMS) Experiment Data Record (EDR). Jan 31, 2013.](https://atmos.nmsu.edu/PDS/data/mslrem_0001/DOCUMENT/MSL_REMS_EDR_SIS.PDF)  
- [The Open University. OpenMars Ozone Column Database. February 2019](https://ordo.open.ac.uk/articles/dataset/OpenMARS_ozone_column_database/7315430)
- [Baum, Mark. REMS Data Downloader. Accessed December 4, 2021.](https://github.com/markmbaum/REMS)
- [Programmatic Ponderings. DevOps for DataOps: Building a CI/CD Pipeline for Apache Airflow DAGs](https://programmaticponderings.com/tag/apache-airflow/)

