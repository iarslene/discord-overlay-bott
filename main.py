import discord
from discord.ext import commands
import subprocess

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def progress(ctx):
    await ctx.send("📸 Taking screenshots and extracting progress...")

    # Run your scripts (you can also import them instead of using subprocess)
    subprocess.run(["python3", "take_screenshots.py"])
    result = subprocess.run(["python3", "extract_progress.py"], capture_output=True, text=True)

    # Send the result back to Discord
    await ctx.send(f"```\n{result.stdout[-1900:]}\n```")  # Discord message limit is 2000 chars

bot.run("MTM4NzUyMTIxOTAyMDE5NzkyOA.GcyAYF.8xM5TjNQHW1tJFkZ8dhn8xsj-OJv50AmR_lRBI")
