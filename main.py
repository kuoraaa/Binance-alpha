import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    # Cari channel bernama 'alpha'
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == "alpha":
                await channel.send("✅ Hello from Binance Alpha bot! I'm alive 🚀")
                print(f"Message sent to #{channel.name}")

bot.run(TOKEN)
