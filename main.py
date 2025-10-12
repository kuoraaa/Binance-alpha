import os
import discord
from discord.ext import commands

# Ambil token dari environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("❌ DISCORD_TOKEN tidak ditemukan! Pastikan sudah diatur di Railway Variables.")

# Atur intents agar bot bisa baca pesan
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

# Inisialisasi bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot berhasil login sebagai {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Halo {ctx.author.mention}! 👋 Aku sudah online!")

# Jalankan bot
bot.run(TOKEN)
