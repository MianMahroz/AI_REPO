import pyodbc
import psycopg2
import mysql.connector
from typing import List, Dict, Any
import logging

class DBConnector:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = self._connect()
    
    def _connect(self):
        if self.config['db_type'] == 'mssql':
            return pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.config['host']};"
                f"DATABASE={self.config['database']};"
                f"UID={self.config['username']};"
                f"PWD={self.config['password']}"
            )
        elif self.config['db_type'] == 'postgres':
            return psycopg2.connect(
                host=self.config['host'],
                database=self.config['database'],
                user=self.config['username'],
                password=self.config['password']
            )
        elif self.config['db_type'] == 'mysql':
            return mysql.connector.connect(
                host=self.config['host'],
                database=self.config['database'],
                user=self.config['username'],
                password=self.config['password']
            )
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        cursor = self.connection.cursor()
        cursor.execute(query, params or ())
        self.connection.commit()
        
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return []
    
    def close(self):
        if self.connection:
            self.connection.close()