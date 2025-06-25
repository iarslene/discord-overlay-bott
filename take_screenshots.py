import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import os

# Setup Selenium headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get("https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9")

# Create folder to save slides
os.makedirs("slides", exist_ok=True)

print("[+] Waiting 20 seconds to reach slide 4...")
time.sleep(20)

# Capture slides 4 to 12 (9 total), 5 seconds apart
for i in range(9):
    slide_number = 4 + i
    filename = f"slides/slide{slide_number}.png"
    driver.save_screenshot(filename)
    print(f"[+] Saved {filename}")
    time.sleep(5)

driver.quit()
