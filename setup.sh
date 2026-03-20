#!/bin/bash

echo "========================================"
echo "Mental Stress Assessment - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created."
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [ -d "venv/bin" ]; then
    source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
fi
echo "Virtual environment activated."
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed."
echo ""

# Check if models exist
echo "Checking model files..."
if [ -d "models" ] && [ -f "models/rf_model.joblib" ]; then
    echo "Model files found."
else
    echo "WARNING: Model files not found in models/ directory"
    echo "Make sure to copy your trained models to the models/ folder"
fi
echo ""

# Check if data exists
echo "Checking data files..."
if [ -d "data" ] && [ -f "data/train_recs.csv" ]; then
    echo "Data files found."
else
    echo "WARNING: Data files not found in data/ directory"
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  python app.py"
echo ""
echo "To test the application:"
echo "  python test_app.py"
echo ""
echo "To deploy to Git:"
echo "  git init"
echo "  git add ."
echo "  git commit -m 'Initial commit'"
echo "  git remote add origin YOUR_REPO_URL"
echo "  git push -u origin main"
echo ""
echo "See DEPLOYMENT.md for cloud deployment instructions"
echo ""
