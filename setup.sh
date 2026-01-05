#!/bin/bash

# ERP POC Manager Setup Script
echo "Setting up ERP POC Manager..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create database and run migrations
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Load sample data
echo "Loading sample data..."
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/projects.json
python manage.py loaddata fixtures/candidates.json
python manage.py loaddata fixtures/tasks.json
python manage.py loaddata fixtures/daily_logs.json
python manage.py loaddata fixtures/meetings.json

# Create superuser (optional)
echo "Would you like to create a superuser? (y/n)"
read -r response
if [[ $response =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "Setup complete!"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  http://127.0.0.1:8000/ - Main application"
echo "  http://127.0.0.1:8000/admin/ - Admin panel"
echo ""
echo "Sample users (password: admin123):"
echo "  admin - Project Lead"
echo "  john_dev - Developer"
echo "  sarah_qa - QA Engineer"
echo "  mike_backend - Backend Developer"
echo "  lisa_frontend - Frontend Developer"
echo ""