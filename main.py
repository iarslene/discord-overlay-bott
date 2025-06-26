import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_png_files_from_root():
    return [f for f in os.listdir(".") if f.lower().endswith(".png")]

def extract_text_from_files(image_files):
    all_text = []
    for filepath in image_files:
        if not os.path.exists(filepath):
            all_text.append(f"⚠️ File not found: {filepath}\n{'-'*40}\n")
            continue
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            all_text.append(f"{filepath}:\n{text.strip()}\n{'-'*40}\n")
        except Exception as e:
            all_text.append(f"⚠️ Error reading {filepath}: {e}\n{'-'*40}\n")
    return "\n".join(all_text)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def progress(ctx):
    await ctx.send("🔍 Extracting text from all PNG images in the repo...")

    image_files = get_png_files_from_root()
    if not image_files:
        await ctx.send("⚠️ No PNG files found in the root directory.")
        return

    extracted_text = extract_text_from_files(image_files)

    if not extracted_text.strip():
        extracted_text = "No text detected in the available images."

    for i in range(0, len(extracted_text), 1900):
        await ctx.send(f"```{extracted_text[i:i+1900]}```")

bot.run(os.getenv("DISCORD_TOKEN"))




