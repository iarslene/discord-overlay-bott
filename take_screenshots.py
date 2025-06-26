import time
import os
from playwright.sync_api import sync_playwright
from PIL import Image
import pytesseract

URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

def take_screenshots_and_ocr():
    os.makedirs("slides", exist_ok=True)
    all_text = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(URL)

        print("[+] Waiting 20 seconds for overlay animation...")
        time.sleep(20)

        for i in range(9):
            slide_number = 4 + i
            filename = f"slides/slide{slide_number}.png"
            page.screenshot(path=filename)
            print(f"[+] Saved screenshot {filename}")

            image = Image.open(filename)
            text = pytesseract.image_to_string(image)
            all_text.append(f"Slide {slide_number}:\n{text.strip()}\n{'-'*40}\n")

            time.sleep(5)

        browser.close()
    return "\n".join(all_text)

if __name__ == "__main__":
    result = take_screenshots_and_ocr()
    print(result)
