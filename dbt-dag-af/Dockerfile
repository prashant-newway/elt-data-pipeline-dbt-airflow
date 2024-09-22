FROM quay.io/astronomer/astro-runtime:12.1.0

RUN python -m venv .venv-dbt-af && source .venv-dbt-af/bin/activate && \
    pip install --no-cache-dir dbt-snowflake && deactivate
