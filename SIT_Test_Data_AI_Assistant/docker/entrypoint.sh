#!/bin/bash

# Wait for dependencies if needed
# while ! nc -z $DB_HOST $DB_PORT; do sleep 1; done

streamlit run ui/app.py --server.port=$STREAMLIT_SERVER_PORT --server.address=0.0.0.0