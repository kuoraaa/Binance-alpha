import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("❌ DISCORD_TOKEN tidak ditemukan! Pastikan sudah diatur di Railway Variables.")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot berhasil login sebagai {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Halo {ctx.author.mention}! 👋 Aku sudah online!")

bot.run(TOKEN)
