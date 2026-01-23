#!/bin/bash
# Setup script for CV generation project

set -e

echo "Setting up The Most LLM-Friendly CV Ever project..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv the-most-llm-friendly-cv-ever

# Activate virtual environment
echo "Activating virtual environment..."
source the-most-llm-friendly-cv-ever/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source the-most-llm-friendly-cv-ever/bin/activate"
echo ""
echo "To generate your CV, run:"
echo "  python main.py"
echo ""
