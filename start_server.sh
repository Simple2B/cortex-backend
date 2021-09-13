#!/bin/bash
echo Starting server
export POSTGRES_SERVER=db
export POSTGRES_PORT=5432
uvicorn app.main:app --workers 3 --host 0.0.0.0 --port 80
