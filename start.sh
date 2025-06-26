#!/bin/bash
apt-get update && apt-get install -y tesseract-ocr
playwright install-deps
playwright install chromium
python3 main.py

