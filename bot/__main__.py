import discord
from discord.ext import commands
import os
import json

with open("./config/stuff.json") as f:
    bot_config = json.load(f)

with open("./secret") as e:
    TOKEN = e.read().strip()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=['.', '. '], status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='THE Space'), intents=intents)

@bot.listen()
async def on_ready():
    for filename in os.listdir('./bot/extensions'):
        if filename.endswith('.py'):
            await bot.load_extension(f'bot.extensions.{filename[:-3]}')
    channel = await bot.fetch_channel(bot_config["logging"]["startup"])
    await channel.send("Bot has started")

bot.run(TOKEN)