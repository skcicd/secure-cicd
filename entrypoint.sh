#!/bin/bash
set -e

echo "Starting Flask application..."

# Ensure the database exists before starting
if [ ! -f "/app/instance/app.db" ]; then
    echo "Creating SQLite database..."
    flask db upgrade
fi

# Run the application
exec /opt/venv/bin/python run.py
