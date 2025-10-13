import asyncio
import snscrape.modules.twitter as sntwitter
import discord
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("DISCORD_TOKEN")
TWITTER_USERNAME = "alpha123uk"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_tweet_id = None

async def fetch_latest_tweet():
    global last_tweet_id
    tweets = list(sntwitter.TwitterUserScraper(TWITTER_USERNAME).get_items())
    if tweets:
        latest = tweets[0]
        if last_tweet_id != latest.id:
            last_tweet_id = latest.id
            return f"https://x.com/{TWITTER_USERNAME}/status/{latest.id}"
    return None

@tasks.loop(minutes=1)
async def check_tweets():
    channel = discord.utils.get(bot.get_all_channels(), name="alpha")
    tweet_link = await fetch_latest_tweet()
    if tweet_link:
        await channel.send(f"🐦 New tweet from @{TWITTER_USERNAME}!\n{tweet_link}")
        print("✅ Sent tweet link to Discord")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    check_tweets.start()

bot.run(TOKEN)
