import os
import requests
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from xml.etree import ElementTree as ET

# Load environment variables
load_dotenv()

print("🧠 Environment check:")
print("DISCORD_TOKEN:", os.getenv("DISCORD_TOKEN"))
print("DISCORD_CHANNEL_ID:", os.getenv("DISCORD_CHANNEL_ID"))
print("TWITTER_USERNAME:", os.getenv("TWITTER_USERNAME"))

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME", "alpha123uk")

if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID:
    raise ValueError("❌ Missing DISCORD_TOKEN or DISCORD_CHANNEL_ID in environment variables")

DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID)

# Discord setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_tweet_url = None

# Nitter mirrors list
NITTER_MIRRORS = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.freedit.eu"
]

def get_latest_tweet(username):
    """Fetch the latest tweet from multiple Nitter mirrors with automatic rotation."""
    for mirror in NITTER_MIRRORS:
        rss_url = f"{mirror}/{username}/rss"
        try:
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            first_item = root.find("channel/item")
            if first_item is not None:
                link = first_item.find("link").text
                title = first_item.find("title").text
                return {"title": title, "link": link}
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                print(f"⚠️ Rate limited on {mirror}, trying next mirror...")
            else:
                print(f"❌ HTTP error on {mirror}: {http_err}")
        except Exception as e:
            print(f"❌ Failed to fetch from {mirror}: {e}")
    return None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send("✅ Hello from Binance Alpha bot! I'm alive 🚀")
    check_tweets.start()

@tasks.loop(minutes=5.0)
async def check_tweets():
    """Check for new tweets every 5 minutes."""
    global last_tweet_url
    tweet = get_latest_tweet(TWITTER_USERNAME)
    if tweet:
        if tweet["link"] != last_tweet_url:
            print(f"📢 New tweet found: {tweet['title']}")
            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            if channel:
                await channel.send(
                    f"🐦 New tweet from **{TWITTER_USERNAME}**:\n{tweet['title']}\n{tweet['link']}"
                )
            last_tweet_url = tweet["link"]
        else:
            print("⏳ No new tweets yet.")
    else:
        print("⚠️ Could not retrieve tweet from any mirror.")

bot.run(DISCORD_TOKEN)
