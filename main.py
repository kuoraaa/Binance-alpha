import os
import discord
from discord.ext import commands

# Ambil token dari environment variable (Railway)
TOKEN = os.getenv("MTQyNjkyNzgzNjIwMzE4ODM5Nw.Gookgp.DYIDlCA4EmJxtPOpIcDs161moKg90ukzx2DCd0")

# Cek apakah token ditemukan
if TOKEN is None:
    raise ValueError("❌ DISCORD_TOKEN tidak ditemukan! Pastikan sudah diatur di Railway Variables.")

# Mengatur intents (izin bot)
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # penting untuk bisa membaca isi pesan

# Membuat instance bot dengan prefix '!'
bot = commands.Bot(command_prefix="!", intents=intents)

# Event ketika bot siap digunakan
@bot.event
async def on_ready():
    print(f"✅ Bot berhasil login sebagai {bot.user}")

# Contoh command sederhana: !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Halo {ctx.author.mention}! 👋 Aku sudah online!")

# Jalankan bot
bot.run(TOKEN)
