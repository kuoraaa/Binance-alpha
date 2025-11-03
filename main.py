import os
import asyncio
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME", "binance")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_tweet_link = None  # to track the most recent tweet


def get_latest_tweet(username):
    """Scrape latest tweet using Nitter"""
    try:
        url = f"https://nitter.privacydev.net/{username}"
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print("Nitter server error:", res.status_code)
            return None, None

        soup = BeautifulSoup(res.text, "html.parser")
        tweet = soup.find("div", {"class": "timeline-item"})
        if not tweet:
            return None, None

        content = tweet.find("div", {"class": "tweet-content"}).text.strip()
        link = tweet.find("a", {"class": "tweet-date"})["href"]
        full_link = f"https://x.com{link}"
        return content, full_link
    except Exception as e:
        print("Error scraping:", e)
        return None, None


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    check_tweets.start()  # start background loop


@tasks.loop(minutes=2)
async def check_tweets():
    global last_tweet_link
    content, link = get_latest_tweet(TWITTER_USERNAME)
    if not link or not content:
        return

    # Only post if there's a new tweet
    if last_tweet_link != link:
        last_tweet_link = link
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            msg = f"🕊️ New tweet from **@{TWITTER_USERNAME}**:\n\n{content}\n\n{link}"
            await channel.send(msg)
            print("✅ Posted new tweet to Discord!")
        else:
            print("⚠️ Channel not found!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("!ping"):
        await message.channel.send("✅ I'm alive!")


client.run(DISCORD_TOKEN)
