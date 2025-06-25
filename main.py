import discord
from discord.ext import commands
import subprocess
import os

intents = discord.Intents.default()
intents.message_content = True  # Needed for command handling

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def progress(ctx):
    await ctx.send("📸 Taking screenshots and extracting progress...")

    try:
        # Run screenshot script
        subprocess.run(["python", "take_screenshots.py"], check=True)

        # Run extract script and capture output
        result = subprocess.run(["python", "extract_progress.py"], capture_output=True, text=True, check=True)

        output = result.stdout.strip()
        if not output:
            output = "No progress data found."

        # Send result (trim to Discord's message limit)
        await ctx.send(f"```\n{output[-1900:]}\n```")

    except subprocess.CalledProcessError as e:
        await ctx.send("⚠️ Error while processing scripts.")
        print("Script error:", e)

# Use token from Railway env variables
bot.run(os.getenv("DISCORD_TOKEN"))
