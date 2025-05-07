import re

class RuleEngine:
    def __init__(self, system_connectors):
        self.connectors = system_connectors
    
    def process_request(self, intent, user_input):
        try:
            if intent == "get_elife_account":
                return self._handle_get_elife_account()
            elif intent == "remove_account_from_party":
                account = self._extract_account(user_input)
                return self._handle_remove_account_from_party(account)
            elif intent == "add_account_to_party":
                account = self._extract_account(user_input)
                return self._handle_add_account_to_party(account)
            elif intent == "whitelist_number":
                number = self._extract_number(user_input)
                return self._handle_whitelist_number(number)
            elif intent == "get_free_numbers":
                return self._handle_get_free_numbers()
            else:
                return {"error": "Unknown intent"}
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_account(self, text):
        match = re.search(r'account\s+([A-Z0-9]{8,12})', text, re.IGNORECASE)
        if match:
            return match.group(1)
        raise ValueError("No account number found in request")
    
    def _extract_number(self, text):
        match = re.search(r'number\s+([0-9]{10,15})', text, re.IGNORECASE)
        if match:
            return match.group(1)
        raise ValueError("No number found in request")
    
    def _handle_get_elife_account(self):
        return self.connectors.get_elife_account()
    
    def _handle_remove_account_from_party(self, account):
        return self.connectors.remove_account_from_party(account)
    
    def _handle_add_account_to_party(self, account):
        return self.connectors.add_account_to_party(account)
    
    def _handle_whitelist_number(self, number):
        return self.connectors.whitelist_number_in_rtf(number)
    
    def _handle_get_free_numbers(self):
        return self.connectors.get_free_numbers_from_css(3)