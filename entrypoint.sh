#!/bin/bash
set -e

echo "Starting Flask application..."

# Ensure the instance directory exists
mkdir -p /app/instance

# Activate the virtual environment
source /opt/venv/bin/activate

# Set environment variables explicitly
export FLASK_APP=app.py
export FLASK_ENV=production

# Ensure database migrations are applied
if [ ! -f "/app/instance/app.db" ]; then
    echo "Creating SQLite database..."
    
    # Check if migrations exist before running upgrade
    if [ -d "/app/migrations" ]; then
        flask db upgrade
    else
        echo "No migrations found, skipping database upgrade."
    fi
fi

# Run the application
exec python run.py
