#!/bin/bash

# Install OCR engine
apt-get update && apt-get install -y tesseract-ocr

# Install system libraries needed by Playwright browsers
playwright install-deps

# Install Chromium for Playwright
playwright install chromium

# Run your bot
python3 main.py

