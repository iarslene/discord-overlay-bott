import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# ✅ Auto-install the correct chromedriver version
chromedriver_autoinstaller.install()

# ✅ Create directory
os.makedirs("slides", exist_ok=True)

# ✅ Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# ✅ Start driver
driver = webdriver.Chrome(options=options)
driver.get("https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9")

print("[+] Waiting 20 seconds to reach slide 4...")
time.sleep(20)

# ✅ Take 9 slides
for i in range(9):
    slide_number = 4 + i
    filename = f"slides/slide{slide_number}.png"
    driver.save_screenshot(filename)
    print(f"[+] Saved {filename}")
    time.sleep(5)

driver.quit()
