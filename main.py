import discord
from discord.ext import commands
from playwright.async_api import async_playwright
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

OVERLAY_URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

async def take_screenshots_and_ocr():
    os.makedirs("slides", exist_ok=True)
    extracted_text = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(OVERLAY_URL)

        print("[+] Waiting 20 seconds for overlay to load first slide...")
        await asyncio.sleep(20)

        for i in range(3):
            slide_number = 4 + i
            filename = f"slides/slide{slide_number}.png"
            await page.screenshot(path=filename)
            print(f"[+] Saved screenshot {filename}")

            # Precise OCR pre-processing
            image = Image.open(filename)
            image = image.resize((image.width * 2, image.height * 2))
            image = image.convert("L")
            image = ImageEnhance.Contrast(image).enhance(3)
            image = image.filter(ImageFilter.SHARPEN)

            text = pytesseract.image_to_string(image)
            extracted_text.append(f"Slide {slide_number}:\n{text.strip()}\n{'-'*40}\n")

            await asyncio.sleep(10)  # Wait before capturing next slide

        await browser.close()

    return "\n".join(extracted_text)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def progress(ctx):
    await ctx.send("📸 Taking screenshots and extracting text... This may take up to a minute.")

    try:
        result = await take_screenshots_and_ocr()
        if not result.strip():
            result = "❌ No text extracted from slides."

        for chunk in [result[i:i+1900] for i in range(0, len(result), 1900)]:
            await ctx.send(f"```{chunk}```")

    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")
        print("Error:", e)

bot.run(os.getenv("DISCORD_TOKEN"))
