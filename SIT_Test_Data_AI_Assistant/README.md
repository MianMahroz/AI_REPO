# SIT Test Data AI Assistant

## Setup
1. Copy `.env.example` to `.env` and fill in credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run ui/app.py`

## Docker
```bash
docker build -t test-assistant .
docker run -p 8501:8501 --env-file .env test-assistant



# Set up  local environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run ui/app.py


User Input
   ↓
Intent Classifier (BERT)
   ↓
Rule Engine
   ↓
Data Generator / Fetcher
   ↓
System Connectors (API / DB / Mock)
   ↓
5 Backend Systems (SIT)