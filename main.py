import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Files are in repo root
FILES_TO_READ = [
    "slide4.png",
    "slide5.png",
    "slide6.png"
]

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
    await ctx.send("🔍 Extracting text from specified images...")

    extracted_text = extract_text_from_files(FILES_TO_READ)

    if not extracted_text.strip():
        extracted_text = "No text detected in the specified images."

    # Send in chunks to respect Discord message length limits (~2000 chars)
    for i in range(0, len(extracted_text), 1900):
        await ctx.send(f"```{extracted_text[i:i+1900]}```")

bot.run(os.getenv("DISCORD_TOKEN"))


