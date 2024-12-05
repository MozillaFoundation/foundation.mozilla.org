#!/bin/bash

# Set variables for default superuser credentials
SUPERUSER_USERNAME="admin"
SUPERUSER_EMAIL="admin@example.com"
SUPERUSER_PASSWORD="admin"

# Function to kill existing `python manage.py runserver` processes
kill_runserver() {
    echo "Checking for existing 'python manage.py runserver' processes..."
    RUNSERVER_PID=$(ps aux | grep 'python manage.py runserver' | grep -v grep | awk '{print $2}')
    if [ -n "$RUNSERVER_PID" ]; then
        echo "Terminating 'python manage.py runserver' processes..."
        kill -9 $RUNSERVER_PID
        echo "Processes terminated."
    else
        echo "No 'python manage.py runserver' processes found."
    fi
}

# Remove existing environment and project if they exist
echo "Cleaning up previous environment..."
rm -rf ./env/

# Create a new virtual environment inside the project directory
echo "Creating virtual environment..."
python -m venv ./env/
source ./env/bin/activate

# Install project dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Remove the existing SQLite database (if any)
echo "Removing existing database..."
rm -f db.sqlite3

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create a superuser non-interactively
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username="$SUPERUSER_USERNAME").exists():
    User.objects.create_superuser(
        username="$SUPERUSER_USERNAME",
        email="$SUPERUSER_EMAIL",
        password="$SUPERUSER_PASSWORD"
    )
EOF

# Start the development server
echo "Starting development server..."
python manage.py runserver
