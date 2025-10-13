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

# --- Ambil tweet terbaru ---
async def fetch_latest_tweet():
    global last_tweet_id
    tweets = list(sntwitter.TwitterUserScraper(TWITTER_USERNAME).get_items())

    if tweets:
        latest = tweets[0]
        if last_tweet_id != latest.id:
            last_tweet_id = latest.id
            return f"https://x.com/{TWITTER_USERNAME}/status/{latest.id}"

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
