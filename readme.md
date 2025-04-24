# ELT Pipeline with dbt, Snowflake & Airflow
This project demonstrates how to build a robust ELT (Extract, Load, Transform) pipeline using modern data stack tools:

Snowflake for cloud data warehousing

dbt (Data Build Tool) for transformation and testing

Apache Airflow for orchestration

# Tech Stack

Tool	Purpose
Snowflake	Scalable data warehouse
dbt	SQL-based transformation layer
Airflow	Workflow orchestration
Docker	Environment consistency

# Architecture Overview
Extract & Load: Data is sourced from Snowflake's sample datasets (e.g., TPCH_SF1) and made available for transformation.

Transform: dbt is used to define, test, and build data models. This includes staging, intermediate, and mart layers.

Orchestrate: Airflow schedules and manages dbt runs as part of a DAG.

# Getting Started
Step 1: Setup Snowflake
Provision a dedicated warehouse, database, role, and schema for dbt transformations.

Assign proper grants to ensure secure access.


Step 2: Configure dbt Profile
Define how dbt connects to Snowflake via the profiles.yml file.

Assign appropriate warehouses to your models depending on their layer (e.g., view vs table materializations).

Step 3: Define Sources & Staging
Declare raw source tables in a YAML file (sources.yml).

Build staging models to clean, rename, and standardize raw data fields.

Include constraints and relationships through dbt's testing framework.

Step 4: Write Reusable Macros
Use dbt macros to encapsulate logic and avoid repetition (e.g., discount calculations).

Step 5: Build Data Models
Create intermediate models for business logic joins and transformations.

Generate fact tables (e.g., fct_orders) that summarize relevant metrics.

Step 6: Validate with Tests
Use generic tests (not null, unique, referential integrity).

Create singular tests (custom SQL assertions for business rules).

Step 7: Deploy via Airflow
Install dbt-snowflake and Airflow dependencies in Docker.

Create and configure a Snowflake connection in Airflow.

Use Cosmos to orchestrate dbt runs within a DAG.

# Project Structure
```
.
├── dbt-dag-af
│   ├── dags
│   │   └── dbt_dag.py
│   ├── Dockerfile
│   ├── include
│   │   └── dbt_elt_pipeline
│   │       ├── analyses
│   │       ├── dbt_project.yml
│   │       ├── macros
│   │       │   └── pricing.sql
│   │       ├── models
│   │       │   ├── marts
│   │       │   │   ├── fct_orders.sql
│   │       │   │   ├── generic_tests.yml
│   │       │   │   ├── int_order_items_summary.sql
│   │       │   │   └── int_order_items.sql
│   │       │   └── staging
│   │       │       ├── stg_tpch_line_items.sql
│   │       │       ├── stg_tpch_orders.sql
│   │       │       └── tpch_sources.yml
│   │       ├── package-lock.yml
│   │       ├── packages.yml
│   │       ├── README.md
│   │       ├── seeds
│   │       ├── snapshots
│   │       ├── snowflake_script.txt
│   │       └── tests
│   │           ├── fct_orders_date_valid.sql
│   │           └── fct_orders_discount.sql
│   ├── logs
│   │   └── dbt.log
│   ├── packages.txt
│   ├── README.md
│   ├── requirements.txt
│   └── tests
│       └── dags
│           └── test_dag_example.py
├── logs
│   └── dbt.log
├── readme.md
└── tree.txt

17 directories, 25 files

```

# Prerequisites
- A Snowflake account

- Docker (with Compose)

- Apache Airflow

- dbt CLI

# Features
Modular dbt models: Staging → Intermediate → Fact tables

Test-driven development: Generic & custom validations

Reusable macros for DRY transformations

Scheduled DAGs with Cosmos for easy Airflow integration

# Resources
dbt Documentation

Snowflake Documentation

Airflow Docs

Astronomer Cosmos