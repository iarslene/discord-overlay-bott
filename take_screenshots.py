import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

# ✅ Make sure slides directory exists
os.makedirs("slides", exist_ok=True)

# ✅ Chrome options for Railway
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# ✅ Set the ChromeDriver service
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# ✅ Your overlay URL
driver.get("https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9")

print("[+] Waiting 20 seconds to reach slide 4...")
time.sleep(20)

# ✅ Capture slides 4 to 12
for i in range(9):
    slide_number = 4 + i
    filename = f"slides/slide{slide_number}.png"
    driver.save_screenshot(filename)
    print(f"[+] Saved {filename}")
    time.sleep(5)

driver.quit()
