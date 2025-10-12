import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("MTQyNjkyNzgzNjIwMzE4ODM5Nw.Gookgp.DYIDlCA4EmJxtPOpIcDs161moKg90ukzx2DCd0")
CHANNEL_NAME = "alpha"
TWITTER_URL = "https://x.com/alpha123uk"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_tweet = None  # Menyimpan link tweet terakhir


def get_latest_tweet_url():
    """Ambil URL tweet terbaru dari profil X"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(TWITTER_URL, headers=headers)
    if response.status_code != 200:
        print("❌ Gagal mengakses halaman Twitter")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/status/" in href:
            return "https://x.com" + href
    return None


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    check_tweets.start()


@tasks.loop(seconds=60)  # cek setiap 1 menit
async def check_tweets():
    global last_tweet
    tweet_url = get_latest_tweet_url()
    if not tweet_url:
        return

    if last_tweet != tweet_url:
        last_tweet = tweet_url
        print(f"🚨 New Tweet detected: {tweet_url}")
        for guild in client.guilds:
            for channel in guild.text_channels:
                if channel.name == CHANNEL_NAME:
                    await channel.send(f"🚨 New Tweet from @alpha123uk\n🔗 {tweet_url}")
                    return


client.run(TOKEN)
