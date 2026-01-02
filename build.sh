#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Initializing database..."
python << END
from app import app, db
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
END

echo "Build completed!"