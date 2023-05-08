#!/bin/bash

sleep 10
alembic upgrade head
cd website
gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
