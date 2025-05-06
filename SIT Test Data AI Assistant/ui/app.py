import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))


import streamlit as st
from src.intent_classifier import classify_intent
from src.rule_engine import RuleEngine
from src.system_connectors import SystemConnectors

def main():
    st.title("SIT Test Data Assistant")
    user_input = st.text_input("Enter your request:")
    
    if user_input:
        intent = classify_intent(user_input)
        print("INTENT IDENTIFIED",intent);
        engine = RuleEngine(SystemConnectors())
        result = engine.process_request(intent, user_input)
        st.json(result)

if __name__ == "__main__":
    main()