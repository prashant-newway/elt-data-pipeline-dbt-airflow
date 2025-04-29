# ELT Pipeline with dbt, Snowflake & Airflow
This project builds a robust ELT (Extract, Load, Transform) pipeline using industry-standard tools. The pipeline 
1. extracts data from Snowflake's sample datasets, 
2. transforms it using dbt, 
3. and orchestrates the workflow with Apache Airflow.

# Prerequisites
- Snowflake account
Required for creating warehouses, databases, and running queries.

- Docker
To containerize and run the Airflow environment locally.

- Apache Airflow (via Astronomer Cosmos)
Used for scheduling and orchestrating dbt jobs.

- dbt CLI (dbt-snowflake)
For running and testing dbt models locally and in the pipeline.

# Features
- Modular dbt models: Staging → Intermediate → Fact tables

- Test-driven development: Generic & custom validations

- Reusable macros for DRY transformations

- Scheduled DAGs with Cosmos for easy Airflow integration and Pipeline orchestration


# ELT Data Flow

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│  Extract & Load   │────▶│     Transform     │────▶│      Outputs      │
│   (Snowflake)     │     │      (dbt)        │     │   (Fact Tables)   │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
                                   ▲                         
                                   │                         
                          ┌────────┴──────────┐              
                          │                   │              
                          │    Orchestrate    │              
                          │    (Airflow)      │              
                          │                   │              
                          └───────────────────┘              
```

## Process Overview

1. **Extract & Load**
   - Source data from Snowflake's sample datasets (TPCH_SF1)( https://docs.snowflake.com/en/user-guide/sample-data-tpch )

2. **Transform with dbt**
   - **Staging Layer**: Clean, rename, standardize fields

   - **Intermediate Layer**: Apply business logic, joins, transformations
   - **Mart Layer**: Generate fact tables with relevant metrics

3. **Orchestrate with Airflow**
   - Schedule and manage dbt runs as part of DAG
   - Utilize Cosmos for dbt orchestration


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


## Implementation Steps

1. **Setup Snowflake**
   - Provision warehouse, database, role, schema
   - Configure security with proper grants

2. **Configure dbt Profile**
   - Define Snowflake connection in profiles.yml
   - Assign appropriate warehouses to models

3. **Define Sources & Staging**
   - Create source and staging files
    - yml source file:
    ```
    version: 2

sources:
  - name: tpch
    database: snowflake_sample_data
    schema: tpch_sf1
    tables:
      - name: orders
        columns:
          - name: o_orderkey
            tests:
              - unique
              - not_null
      - name: lineitem
        columns:
          - name: l_orderkey
            tests:
              - relationships:
                  to: source('tpch', 'orders')
                  field: o_orderkey

```
    -  staging models models/staging/stg_tpch_orders.sql
   ```
   select
    o_orderkey as order_key,
    o_custkey as customer_key,
    o_orderstatus as status_code,
    o_totalprice as total_price,
    o_orderdate as order_date
from
    {{ source('tpch', 'orders') }}

```
- For models/staging/tpch/stg_tpch_line_items.sql
```
select
    {{
        dbt_utils.generate_surrogate_key([
            'l_orderkey',
            'l_linenumber'
        ])
    }} as order_item_key,
	l_orderkey as order_key,
	l_partkey as part_key,
	l_linenumber as line_number,
	l_quantity as quantity,
	l_extendedprice as extended_price,
	l_discount as discount_percentage,
	l_tax as tax_rate
from
    {{ source('tpch', 'lineitem') }}
```



4. **Write Reusable Macros**
   - Create dbt macros for common logic

5. **Build Data Models**
   - Develop intermediate  and fact tables

6. **Validate with Tests**
   - Implement generic tests 

7. **Deploy via Airflow**
   - Install dependencies in Docker
   - Configure Snowflake connection
   - Use Cosmos to orchestrate dbt runs



# References:
- [dbt Documentation](https://docs.getdbt.com/docs/build/documentation)

- https://docs.snowflake.com/en/


- [Astronomer Cosmos](https://github.com/astronomer/astronomer-cosmos/)