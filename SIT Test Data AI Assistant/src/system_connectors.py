import os
import requests
from typing import Dict, Any, List
from .db_connector import DBConnector
from .db_queries import TestDataQueries
from configparser import ConfigParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SystemConnectors:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config/config.ini')
        
        # Initialize DB connections
        self.db_connections = {
            "css": self._init_db_connection('database.css'),
            "rtf": self._init_db_connection('database.rtf'),
            "party": self._init_db_connection('database.party')
        }
        
        # API configuration
        self.api_config = {
            "css": {
                "base_url": self.config.get('api', 'css_base_url'),
                "token": os.getenv('CSS_API_TOKEN')
            },
            "rtf": {
                "base_url": self.config.get('api', 'rtf_base_url'),
                "token": os.getenv('RTF_API_TOKEN')
            },
            "party": {
                "base_url": self.config.get('api', 'party_base_url'),
                "token": os.getenv('PARTY_API_TOKEN')
            }
        }

    def _init_db_connection(self, section: str) -> DBConnector:
        """Initialize a database connection from config"""
        db_config = {
            "db_type": self.config.get(section, 'db_type'),
            "host": self.config.get(section, 'host'),
            "database": self.config.get(section, 'database'),
            "username": self.config.get(section, 'username'),
            "password": os.getenv(f"{section.split('.')[-1].upper()}_DB_PASSWORD")
        }
        return DBConnector(db_config)

    # API Methods
    def get_elife_account(self) -> Dict[str, Any]:
        """Get eLife account via API"""
        return self._make_api_call("css", "accounts/elife")

    def whitelist_number(self, number: str) -> Dict[str, Any]:
        """Whitelist number via API"""
        return self._make_api_call("rtf", "whitelist", method="POST", data={"number": number})

    # Database Methods
    def db_get_elife_account(self) -> Dict[str, Any]:
        """Get eLife account directly from database"""
        with self.db_connections["css"] as db:
            result = db.execute_query(TestDataQueries.get_free_elife_accounts())
            return result[0] if result else {"error": "No accounts available"}

    def db_whitelist_number(self, number: str) -> Dict[str, Any]:
        """Whitelist number directly in database"""
        with self.db_connections["rtf"] as db:
            result = db.execute_query(TestDataQueries.whitelist_number(), (number,))
            return {"status": "success", "id": result[0]["id"]}

    # Helper Methods
    def _make_api_call(self, system: str, endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
        url = f"{self.api_config[system]['base_url']}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_config[system]['token']}"}
        
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def close_all(self):
        """Close all database connections"""
        for conn in self.db_connections.values():
            conn.close()