from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

# Prepare save folder
URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"
SAVE_DIR = "slides"
os.makedirs(SAVE_DIR, exist_ok=True)

# Set up Chrome options
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,720")

# Use Railway's chromedriver path
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

driver.get(URL)
time.sleep(5)

for i in range(1, 13):
    screenshot_path = os.path.join(SAVE_DIR, f"slide{i}.png")
    driver.save_screenshot(screenshot_path)
    print(f"📸 Saved: {screenshot_path}")
    time.sleep(1)

driver.quit()
