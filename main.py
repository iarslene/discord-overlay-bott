import time
import os
from playwright.sync_api import sync_playwright
from PIL import Image
import pytesseract

# URL of your StreamElements overlay
URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

# Directory for screenshots and OCR text output
os.makedirs("slides", exist_ok=True)
os.makedirs("ocr_text", exist_ok=True)

def screenshot_and_ocr():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(URL)

        print("[+] Waiting 20 seconds for overlay animation to reach slide 4...")
        time.sleep(20)

        for i in range(9):
            slide_number = 4 + i
            filename = f"slides/slide{slide_number}.png"
            ocr_filename = f"ocr_text/slide{slide_number}.txt"

            # Take screenshot
            page.screenshot(path=filename)
            print(f"[+] Saved screenshot {filename}")

            # OCR extraction
            image = Image.open(filename)
            text = pytesseract.image_to_string(image)

            # Save OCR result
            with open(ocr_filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[+] Saved OCR text {ocr_filename}")

            time.sleep(5)  # wait before next slide

        browser.close()

if __name__ == "__main__":
    screenshot_and_ocr()
