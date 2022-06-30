import discord
import json
from discord.ext import commands

ephemeral = discord.MessageFlags.ephemeral

with open('./config/stuff.json') as e:
    bot_config = json.load(e)

class utility(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=['Ping'], description='Shows the latency of the bot')
    async def _ping(self, ctx):
        await ctx.send(f'Latency :- `{round(self.bot.latency * 1000)} ms`')

    @commands.command(name='av', description='Shows the avatar of someone', aliases=['avatar'])
    async def _av(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.message.author
    
        embed = discord.Embed(color=0x3498db, title=f"{member}'s avatar")
        embed.set_image(url=member.display_avatar)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['Embed'], name='embed', description='Creates an embed, separate the title from the description with |')
    async def _embed(self, ctx, text):
        channel = ctx.channel

        try:
            title, description = text.split("|", 1)
            embed = discord.Embed(title=title, description=description, color=0x3498db)
            await channel.send(embed=embed)
            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            raise e

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        utility(bot),
        guilds = [discord.Object(id = 837616575976177727)]
    )