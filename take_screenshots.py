import os
import asyncio
from playwright.async_api import async_playwright

URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

async def take_screenshots():
    os.makedirs("slides", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(URL)

        print("[+] Waiting 20 seconds to reach first slide...")
        await asyncio.sleep(20)

        for i in range(3):
            slide_number = i + 1
            filename = f"slides/slide{slide_number}.png"
            await page.screenshot(path=filename)
            print(f"[+] Saved {filename}")
            await asyncio.sleep(10)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(take_screenshots())

