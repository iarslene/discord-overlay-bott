#!/bin/bash

# Update packages and install Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr

# Install Playwright Chromium browser
playwright install chromium

# Run your Discord bot
python3 main.py
