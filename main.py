import os
import discord
from discord.ext import commands
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Optional: adjust path
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def preprocess_image(path):
    image = Image.open(path)
    image = image.resize((image.width * 3, image.height * 3))  # Upscale
    image = image.convert("L")  # Grayscale
    image = ImageEnhance.Contrast(image).enhance(3)  # Contrast
    image = image.filter(ImageFilter.MedianFilter(size=3))  # Denoise
    return image

def extract_text_from_screenshots():
    folder = "slides"
    all_text = []

    for i in range(1, 4):  # slide1 to slide3
        path = os.path.join(folder, f"slide{i}.png")
        if not os.path.exists(path):
            all_text.append(f"⚠️ slide{i}.png not found.")
            continue

        image = preprocess_image(path)
        config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(image, config=config)

        all_text.append(f"Slide {i}:\n{text.strip()}\n{'-'*40}")

    return "\n".join(all_text)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def progress(ctx):
    await ctx.send("🔍 Extracting text from screenshots...")

    try:
        result = extract_text_from_screenshots()
        if not result.strip():
            result = "⚠️ No text detected."

        for i in range(0, len(result), 1900):
            await ctx.send(f"```{result[i:i+1900]}```")

    except Exception as e:
        await ctx.send("⚠️ Error while processing.")
        print("Error:", e)

bot.run(os.getenv("DISCORD_TOKEN"))

