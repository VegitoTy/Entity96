import discord
import aiohttp
from discord.ext import commands
import os
import json

with open("./config/stuff.json") as f:
    bot_config = json.load(f)

with open("./secret") as e:
    TOKEN = e.read().strip()

class Entity(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='.',
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name='THE Space'),
            intents=discord.Intents.all())

    async def setup_hook(self):
        for filename in os.listdir('./bot/extensions'):
            if filename.endswith('.py'):
                extension = f'bot.extensions.{filename[:-3]}'
                await self.load_extension(f"{extension}")
        await bot.tree.sync(guild = discord.Object(id = 837616575976177727))

    async def on_ready(self):
        channel = await self.fetch_channel(bot_config["logging"]["startup"])
        await channel.send("Bot has started")
        print(f'Logged in as {self.user}')

bot = Entity()
bot.run(TOKEN)