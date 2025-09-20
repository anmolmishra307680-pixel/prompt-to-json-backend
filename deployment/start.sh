#!/usr/bin/env bash
set -e

# Environment variables with defaults
PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}
THREADS=${THREADS:-2}
TIMEOUT=${GUNICORN_TIMEOUT:-120}
MAX_REQUESTS=${MAX_REQUESTS:-1000}
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-100}

# Create necessary directories
mkdir -p logs spec_outputs reports

# Set Python path
export PYTHONPATH="/app/src:/app:$PYTHONPATH"

# Database initialization
echo "🔧 Initializing database..."
python -c "import sys; sys.path.insert(0, '/app/src'); from db.database import Database; db = Database(); print('✅ Database ready')"

# Start server
echo "🚀 Starting Prompt-to-JSON API on port $PORT with $WORKERS workers..."

if [ "$PRODUCTION_MODE" = "true" ]; then
    echo "🏭 Production mode enabled"
    exec gunicorn -k uvicorn.workers.UvicornWorker main:app \
        --bind 0.0.0.0:$PORT \
        --workers $WORKERS \
        --threads $THREADS \
        --timeout $TIMEOUT \
        --max-requests $MAX_REQUESTS \
        --max-requests-jitter $MAX_REQUESTS_JITTER \
        --worker-connections 1000 \
        --backlog 2048 \
        --keep-alive 30 \
        --log-level info \
        --access-logfile - \
        --error-logfile -
else
    echo "🔧 Development mode"
    exec uvicorn main:app \
        --host 0.0.0.0 \
        --port $PORT \
        --log-level info \
        --reload
fi