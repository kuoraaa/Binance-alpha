import asyncio
import snscrape.modules.twitter as sntwitter
import discord
from discord.ext import commands, tasks
import os

# Ambil token dari environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
TWITTER_USERNAME = "alpha123uk"

# Setup Discord intents & bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_tweet_id = None

# --- Ambil tweet terbaru (1 saja) ---
async def fetch_latest_tweet():
    global last_tweet_id
    try:
        for tweet in sntwitter.TwitterUserScraper(TWITTER_USERNAME).get_items():
            if last_tweet_id != tweet.id:
                last_tweet_id = tweet.id
                return f"https://x.com/{TWITTER_USERNAME}/status/{tweet.id}"
            break  # ambil 1 tweet saja
    except Exception as e:
        print(f"⚠️ Error saat mengambil tweet: {e}")
    return None

# --- Loop pengecekan tiap 1 menit ---
@tasks.loop(minutes=1)
async def check_tweets():
    await bot.wait_until_ready()
    channel = discord.utils.get(bot.get_all_channels(), name="alpha")
    if not channel:
        print("⚠️ Channel #alpha tidak ditemukan.")
        return

    tweet_link = await fetch_latest_tweet()
    if tweet_link:
        await channel.send(f"🐦 New tweet from @{TWITTER_USERNAME}!\n{tweet_link}")
        print(f"✅ Sent tweet link to Discord: {tweet_link}")

# --- Saat bot siap ---
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    check_tweets.start()

# --- Jalankan bot ---
bot.run(TOKEN)
