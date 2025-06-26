import os
import re
import asyncio
import discord
from discord.ext import commands
from playwright.async_api import async_playwright
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

async def take_screenshots_and_ocr() -> str:
    os.makedirs("slides", exist_ok=True)
    all_text = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(URL)

        # Initial wait so overlay animations can start
        print("[+] Waiting 15 seconds for overlay initial load...")
        await asyncio.sleep(15)

        for idx, slide_num in enumerate(range(4, 13)):
            wait_time = 20 if slide_num == 4 else 10
            print(f"[+] Waiting {wait_time}s before capturing slide {slide_num}")
            await asyncio.sleep(wait_time)

            filename = f"slides/slide{slide_num}.png"
            try:
                await page.screenshot(path=filename)
                print(f"[+] Saved {filename}")
            except Exception as e:
                print(f"⚠️ Failed to save {filename}: {e}")
                continue

            # Ensure file is available
            for _ in range(5):
                if os.path.exists(filename):
                    break
                await asyncio.sleep(1)
            else:
                print(f"❌ {filename} not found after screenshot")
                continue

            image = Image.open(filename)
            image = image.resize((image.width * 2, image.height * 2))
            image = image.convert("L")
            image = ImageEnhance.Contrast(image).enhance(2.5)
            image = image.filter(ImageFilter.SHARPEN)

            text = pytesseract.image_to_string(image)
            all_text.append(f"Slide {slide_num}:\n{text.strip()}\n{'-'*40}\n")

        # Extra buffer before closing
        await asyncio.sleep(5)
        await browser.close()

    return "".join(all_text)

@bot.command()
async def progress(ctx):
    await ctx.send("📸 Capturing overlay slides 4–12 and extracting text… please wait.")

    try:
        extracted = await take_screenshots_and_ocr()
        if not extracted.strip():
            extracted = "No progress text detected."

        for i in range(0, len(extracted), 1900):
            await ctx.send(f"```{extracted[i:i+1900]}```")
    except Exception as e:
        await ctx.send(f"⚠️ Error during processing: {e}")
        print("Error:", e)

bot.run(os.getenv("DISCORD_TOKEN"))





