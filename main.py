import discord
from discord.ext import commands
import os
import time
from playwright.sync_api import sync_playwright
from PIL import Image
import pytesseract

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

URL = "https://streamelements.com/overlay/68598695ad17f766e5f73a53/BxyUCTK-TdLWVe2zHmerlzMa_LhpEL2qcF7voCp9U1TkTMp9"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

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

@bot.command()
async def progress(ctx):
    await ctx.send("📸 Taking screenshots and extracting progress... This may take a while.")

    try:
        extracted_text = take_screenshots_and_ocr()

        if not extracted_text.strip():
            extracted_text = "No progress text detected."

        # Discord message limit ~2000 chars
        for chunk_start in range(0, len(extracted_text), 1900):
            await ctx.send(f"```{extracted_text[chunk_start:chunk_start+1900]}```")

    except Exception as e:
        await ctx.send(f"⚠️ Error during processing: {e}")
        print("Error:", e)

bot.run(os.getenv("DISCORD_TOKEN"))
