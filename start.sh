#!/usr/bin/env bash
set -e

PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}
THREADS=${THREADS:-2}
TIMEOUT=${GUNICORN_TIMEOUT:-120}

exec gunicorn -k uvicorn.workers.UvicornWorker main_api:app \
  --bind 0.0.0.0:$PORT \
  --workers $WORKERS \
  --threads $THREADS \
  --timeout $TIMEOUT \
  --log-level info