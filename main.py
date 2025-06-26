import os
import re
import asyncio
import discord
from discord.ext import commands
from playwright.async_api import async_playwright
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Adjust if needed

URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

def preprocess_image_for_ocr(image_path):
    image = Image.open(image_path)
    image = image.resize((image.width * 2, image.height * 2))
    image = image.convert("L")
    image = ImageEnhance.Contrast(image).enhance(3)
    image = image.filter(ImageFilter.SHARPEN)
    return image

async def take_3_slides_and_ocr():
    os.makedirs("slides", exist_ok=True)
    all_text = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(URL)

        print("[+] Waiting 20 seconds for first slide to appear...")
        await asyncio.sleep(20)

        for i in range(3):
            slide_number = i + 1
            filename = f"slides/slide{slide_number}.png"
            await page.screenshot(path=filename)
            print(f"[+] Saved screenshot {filename}")

            image = preprocess_image_for_ocr(filename)
            text = pytesseract.image_to_string(image)
            all_text.append(f"Slide {slide_number}:\n{text.strip()}\n{'-'*40}\n")

            await asyncio.sleep(10)

        await browser.close()

    return "".join(all_text)

@bot.command()
async def progress(ctx):
    await ctx.send("📸 Capturing the first 3 slides... Please wait.")

    try:
        result = await take_3_slides_and_ocr()
        if not result.strip():
            result = "No text detected."

        for chunk_start in range(0, len(result), 1900):
            await ctx.send(f"```{result[chunk_start:chunk_start+1900]}```")

    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")
        print("Error:", e)

bot.run(os.getenv("DISCORD_TOKEN"))
