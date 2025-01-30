#!/bin/bash
set -e

echo "Starting Flask application..."

# Ensure the instance directory exists
#mkdir -p /app/instance

# Set environment variables explicitly
export FLASK_APP=run.py
export FLASK_ENV=production

# Wait for the database (useful for PostgreSQL/MySQL; can be ignored for SQLite)
sleep 2

# Ensure database migrations are applied
if [ ! -f "/app/instance/app.db" ]; then
    echo "Creating SQLite database..."
    flask db upgrade || echo "Skipping migration (no Alembic files)"
fi

# Run the application
#exec /opt/venv/bin/python run.py
python run.py