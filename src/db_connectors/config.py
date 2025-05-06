from decouple import config
from typing import Dict, Any

def get_postgres_config() -> Dict[str, Any]:
    return {
        'host': config('PG_HOST'),
        'database': config('PG_DATABASE'),
        'user': config('PG_USER'),
        'password': config('PG_PASSWORD'),
        'port': config('PG_PORT', default=5432, cast=int)
    }

def get_oracle_config() -> Dict[str, Any]:
    return {
        'host': config('ORACLE_HOST'),
        'service_name': config('ORACLE_SERVICE'),
        'user': config('ORACLE_USER'),
        'password': config('ORACLE_PASSWORD'),
        'port': config('ORACLE_PORT', default=1521, cast=int)
    }

def get_teradata_config() -> Dict[str, Any]:
    return {
        'host': config('TERADATA_HOST'),
        'user': config('TERADATA_USER'),
        'password': config('TERADATA_PASSWORD'),
        'database': config('TERADATA_DATABASE')
    }

def get_snowflake_config() -> Dict[str, Any]:
    return {
        'account': config('SNOWFLAKE_ACCOUNT'),
        'user': config('SNOWFLAKE_USER'),
        'password': config('SNOWFLAKE_PASSWORD'),
        'database': config('SNOWFLAKE_DATABASE'),
        'warehouse': config('SNOWFLAKE_WAREHOUSE'),
        'schema': config('SNOWFLAKE_SCHEMA')
    } 