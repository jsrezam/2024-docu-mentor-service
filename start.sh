#!/bin/bash
# start.sh

cd /docu-mentor-service/documentor/
python3 populate_database.py

uvicorn app_api_handler:app --reload --host 0.0.0.0 --port 8000
