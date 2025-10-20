#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # Exit on error

echo "=========================================="
echo "  Building Wearable Biosignal Backend"
echo "=========================================="

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Build completed successfully!"
