from typing import List, Dict, Any

class TestDataQueries:
    @staticmethod
    def get_free_elife_accounts(limit: int = 1) -> str:
        return f"""
        SELECT account_number 
        FROM css_accounts 
        WHERE account_type = 'ELIFE' 
          AND status = 'AVAILABLE'
        ORDER BY created_date ASC
        LIMIT {limit}
        """
    
    @staticmethod
    def get_free_numbers(limit: int = 3) -> str:
        return f"""
        SELECT phone_number 
        FROM css_numbers 
        WHERE status = 'FREE'
          AND number_type = 'MOBILE'
        ORDER BY RAND()
        LIMIT {limit}
        """
    
    # Other query methods...