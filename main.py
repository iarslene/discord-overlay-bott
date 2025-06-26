import os
import re
import asyncio
import discord
from discord.ext import commands
from playwright.async_api import async_playwright
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Overlay URL
URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# OCR + Screenshot function
async def take_screenshots_and_ocr() -> str:
    os.makedirs("slides", exist_ok=True)
    all_text = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(URL)

        print("[+] Waiting 20 seconds for overlay animation...")
        await asyncio.sleep(20)

        for i in range(9):
            slide_number = 4 + i
            filename = f"slides/slide{slide_number}.png"
            await page.screenshot(path=filename)
            print(f"[+] Saved screenshot {filename}")

            # OCR preprocessing
            image = Image.open(filename)
            image = image.resize((image.width * 2, image.height * 2))      # upscale
            image = image.convert("L")                                     # grayscale
            image = ImageEnhance.Contrast(image).enhance(2.5)              # increase contrast
            image = image.filter(ImageFilter.SHARPEN)                      # sharpen

            text = pytesseract.image_to_string(image)
            all_text.append(f"Slide {slide_number}:\n{text.strip()}\n{'-'*40}\n")

            await asyncio.sleep(5)

        await browser.close()

    return "".join(all_text)

# Discord bot command
@bot.command()
async def progress(ctx):
    await ctx.send("📸 Capturing overlay and extracting progress... Please wait.")

    try:
        extracted = await take_screenshots_and_ocr()

        if not extracted.strip():
            extracted = "No progress text detected."

        # Split long messages for Discord limits
        for i in range(0, len(extracted), 1900):
            await ctx.send(f"```{extracted[i:i+1900]}```")

    except Exception as e:
        await ctx.send(f"⚠️ Error during processing: {e}")
        print("Error:", e)

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))



