import os
import requests
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

# Load environment variables (for local testing or Railway env)
load_dotenv()

print("🧠 Environment check:")
print("DISCORD_TOKEN:", os.getenv("DISCORD_TOKEN"))
print("DISCORD_CHANNEL_ID:", os.getenv("DISCORD_CHANNEL_ID"))
print("TWITTER_USERNAME:", os.getenv("TWITTER_USERNAME"))

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME", "alpha123uk")  # default fallback

# Validate environment
if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID:
    raise ValueError("❌ Missing DISCORD_TOKEN or DISCORD_CHANNEL_ID in environment variables")

# Convert channel ID
DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID)

# --- Discord setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Track last seen tweet
last_tweet_url = None


def get_latest_tweet(username):
    """Scrape latest tweet using a Nitter instance."""
    nitter_url = f"https://nitter.net/{username}/rss"
    try:
        response = requests.get(nitter_url, timeout=10)
        response.raise_for_status()
        from xml.etree import ElementTree as ET

        root = ET.fromstring(response.content)
        first_item = root.find("channel/item")
        if first_item is not None:
            link = first_item.find("link").text
            title = first_item.find("title").text
            return {"title": title, "link": link}
        else:
            print("⚠️ No tweet items found in RSS feed.")
    except Exception as e:
        print(f"❌ Failed to fetch tweets: {e}")
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
    global last_tweet_url
    tweet = get_latest_tweet(TWITTER_USERNAME)
    if tweet:
        if tweet["link"] != last_tweet_url:
            print(f"📢 New tweet found: {tweet['title']}")
            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            if channel:
                await channel.send(f"🐦 New tweet from **{TWITTER_USERNAME}**:\n{tweet['title']}\n{tweet['link']}")
            last_tweet_url = tweet["link"]
        else:
            print("⏳ No new tweets yet.")
    else:
        print("⚠️ Could not retrieve tweet.")


bot.run(DISCORD_TOKEN)
