import os
import requests
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")

if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID or not TWITTER_BEARER_TOKEN or not TWITTER_USERNAME:
    raise ValueError("❌ Missing one or more required environment variables in .env")

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_tweet_id = None

# --- Step 1: Get Twitter user ID ---
def get_twitter_user_id(username):
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["id"]

user_id = get_twitter_user_id(TWITTER_USERNAME)
print(f"Twitter user ID for {TWITTER_USERNAME}: {user_id}")

# --- Step 2: Fetch latest tweet ---
def get_latest_tweet():
    global user_id, TWITTER_BEARER_TOKEN
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5&tweet.fields=created_at"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "data" in data and len(data["data"]) > 0:
            latest_tweet = data["data"][0]
            return {"id": latest_tweet["id"], "text": latest_tweet["text"]}
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch tweets: {e}")
    return None

# --- Discord bot events ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send("✅ Bot is online and ready!")
    check_tweets.start()

# --- Task loop to check tweets ---
@tasks.loop(minutes=5)
async def check_tweets():
    global last_tweet_id
    tweet = get_latest_tweet()
    if tweet:
        if tweet["id"] != last_tweet_id:
            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            if channel:
                await channel.send(f"🐦 New tweet from **{TWITTER_USERNAME}**:\n{tweet['text']}")
            last_tweet_id = tweet["id"]
        else:
            print("⏳ No new tweets yet.")
    else:
        print("⚠️ Could not retrieve tweet.")

# --- Run bot ---
bot.run(DISCORD_TOKEN)
