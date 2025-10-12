import os
import discord
from discord.ext import commands

# Ambil token dari environment variable Railway
TOKEN = os.getenv("DISCORD_TOKEN")

# Inisialisasi intents (wajib diaktifkan agar bot bisa baca pesan, dsb)
intents = discord.Intents.default()
intents.message_content = True  # penting agar bot bisa baca isi pesan

# Inisialisasi bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Event ketika bot berhasil login
@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")

# Contoh perintah sederhana
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! 👋 I'm alive and running on Railway!")

# Jalankan bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ ERROR: DISCORD_TOKEN tidak ditemukan. Pastikan sudah diatur di Railway Variables.")
