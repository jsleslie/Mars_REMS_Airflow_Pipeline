# Mars Curiosity Redshift Data Warehouse & Airflow Pipeline
Udacity Data Engineering Capstone Project

![DAG Testing workflow](https://github.com/jsleslie/Mars_REMS_Airflow_Pipeline/actions/workflows/test_dags.yml/badge.svg)

![S3 Sync workflow](https://github.com/jsleslie/Mars_REMS_Airflow_Pipeline/actions/workflows/sync_dags.yml/badge.svg)


## Project Summary
The goal of this project is to provide an SQL-queryable data warehouse for analysts to analyze data collected from the Mars Curiosity Rover. To this end, the project combines multiple data sets on environmental observations and rover telemetry to organise it into an Amazon Redshift data warehouse via an Apache Airflow managed data pipeline. As part of this work, the data will be uploaded to S3 after which the data will be read from S3, then loaded into staging tables in Redshift before the creation of fact and dimension tables. In the final step, data quality checks are performed on the output tables to verify the health of the pipeline output. 

## Use Cases
This data product may be applied to a range of use cases including:
* Deepening our understanding of Mars' seasonal conditions 
* Providing an accessible resource for the creation of a Rover-centric app delivering visualizations of monthly weather and positional data
* A post-mortem analysis of whether weather-related risks were considered in the planning of rover manouevers

## Queries
Some examples of the kind of queries that may be performed using this data product include:
* Determining the daily extreemes of temperature, pressure, and humidity observed by the rover
* Determining the average horizontal and vertical wind speeds by hour
* Calculating the average horizontal distance covered per day of the mission


## Datasets Used
There are 2 main datasets used from NASA's Planertary Data System on the Mars Curiosity Rover Environment Monitoring Station (REMS) found [here](https://atmos.nmsu.edu/PDS/data/mslrem_1001/):
* **REMS Environment data set**: This data set
* **REMS Ancillary data set**:


## Airflow DAG Overview
An overview of the ETL pipeline is provided in the Directed Acyclic Graph (DAG) below:

![capstone_dag](img/capstone_dag.png)



## References

- [Jet Propulsion Laboratory. Mars Science Laboratory (MSL) Software Interface Specification (SIS) Rover Environmental Monitoring Station (REMS) Experiment Data Record (EDR). Jan 31, 2013.](https://atmos.nmsu.edu/PDS/data/mslrem_0001/DOCUMENT/MSL_REMS_EDR_SIS.PDF)  
- [The Open University. OpenMars Ozone Column Database. February 2019](https://ordo.open.ac.uk/articles/dataset/OpenMARS_ozone_column_database/7315430)
- [Baum, Mark. REMS Data Downloader. Accessed December 4, 2021.](https://github.com/markmbaum/REMS)
- [Programmatic Ponderings. DevOps for DataOps: Building a CI/CD Pipeline for Apache Airflow DAGs](https://programmaticponderings.com/tag/apache-airflow/)

