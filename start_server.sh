#!/bin/bash

# Start Server Script for Wearable Biosignal Analysis Backend
# This script starts the FastAPI server

echo "=========================================="
echo "  Wearable Biosignal Analysis Backend"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   cd backend && ./start_server.sh"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "📦 Checking dependencies..."

# Install dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✓ Dependencies ready"
echo ""

echo "🚀 Starting server..."
echo "   API will be available at: http://localhost:8000"
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 main.py
