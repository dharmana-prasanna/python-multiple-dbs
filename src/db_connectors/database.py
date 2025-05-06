import psycopg2
import cx_Oracle
import teradatasql
import snowflake.connector
from typing import Any, List, Dict
from .config import (
    get_postgres_config,
    get_oracle_config,
    get_teradata_config,
    get_snowflake_config
)

class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

class PostgresConnector(DatabaseConnector):
    def __init__(self):
        super().__init__()
        config = get_postgres_config()
        self.connection = psycopg2.connect(**config)
        self.cursor = self.connection.cursor()

class OracleConnector(DatabaseConnector):
    def __init__(self):
        super().__init__()
        config = get_oracle_config()
        dsn = cx_Oracle.makedsn(
            config['host'],
            config['port'],
            service_name=config['service_name']
        )
        self.connection = cx_Oracle.connect(
            user=config['user'],
            password=config['password'],
            dsn=dsn
        )
        self.cursor = self.connection.cursor()

class TeradataConnector(DatabaseConnector):
    def __init__(self):
        super().__init__()
        config = get_teradata_config()
        self.connection = teradatasql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        self.cursor = self.connection.cursor()

class SnowflakeConnector(DatabaseConnector):
    def __init__(self):
        super().__init__()
        config = get_snowflake_config()
        self.connection = snowflake.connector.connect(**config)
        self.cursor = self.connection.cursor()

def get_connector(db_type: str) -> DatabaseConnector:
    connectors = {
        'postgres': PostgresConnector,
        'oracle': OracleConnector,
        'teradata': TeradataConnector,
        'snowflake': SnowflakeConnector
    }
    
    if db_type not in connectors:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    return connectors[db_type]() 