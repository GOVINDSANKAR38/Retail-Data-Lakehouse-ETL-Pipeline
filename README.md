# Retail Data Lakehouse & ETL Pipeline

## Overview

Retail Data Lakehouse & ETL Pipeline is an end-to-end Data Engineering project that simulates a modern cloud-based analytics platform for retail and e-commerce data.

The project automatically extracts product data from a public API, stores raw data in Amazon S3, processes and transforms data using Apache Spark, performs data quality validations, updates the AWS Glue Data Catalog, and enables analytical querying through Amazon Athena.

The entire pipeline is orchestrated using Apache Airflow and containerized with Docker.

The project automatically extracts product data from a public API, stores raw data in Amazon S3, processes and transforms data using Apache Spark, performs data quality validations, updates the AWS Glue Data Catalog, and enables analytical querying through Amazon Athena.

The entire pipeline is orchestrated using Apache Airflow and containerized with Docker.

---

## Architecture

Public API

↓

Apache Airflow

↓

Amazon S3 (Raw Layer)

↓

Apache Spark ETL

↓

Amazon S3 (Processed Layer)

↓

Data Quality Validation

↓

AWS Glue Crawler

↓

AWS Glue Data Catalog

↓

Amazon Athena

---

## Technologies Used

### Orchestration

* Apache Airflow 2.10

### Processing

* Apache Spark 3.5
* PySpark

### Storage

* Amazon S3

### Metadata Management

* AWS Glue
* AWS Glue Crawler
* AWS Glue Data Catalog

### Query Engine

* Amazon Athena

### Programming

* Python 3.12

### Testing

* Pytest

### Infrastructure

* Docker
* Docker Compose

### Monitoring

* Discord Webhooks

---

## Project Structure

```text
Enterprise_Retail_Data_Lakehouse_Pipeline/

├── dags/
├── scripts/
├── spark_jobs/
├── tests/
├── sql/
├── logs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Pipeline Workflow

### 1. Extract Data

Retrieve product information from a public REST API.

### 2. Load Raw Data

Store JSON files in Amazon S3 Raw Layer.

### 3. Spark ETL

Transform raw data and calculate business metrics.

### 4. Data Quality Checks

Validate:

* Empty datasets
* Missing columns
* Null values
* Negative values

### 5. Glue Crawler

Automatically update the Glue Data Catalog.

### 6. Athena Analytics

Run SQL queries directly on the Data Lake.

---

## Testing

Execute unit tests:

```bash
pytest tests/ -v
```

---

## Initial Setup

Execute Initial Setup:

```bash
mkdir logs

sudo chown -R 50000:0 logs

sudo chmod -R 775 logs
```

---

## Build and start all services:

Execute Build and start all services::

```bash
docker compose up --build -d
```

---


## Monitoring

The project includes Discord notifications for task failures through Airflow callbacks.

---

## Example Analytics

* Products per category
* Average price by category
* Top categories by product volume
* Data quality validation metrics

---



