import discord
import json
from discord.ext import commands

ephemeral = discord.MessageFlags.ephemeral

with open('./config/stuff.json') as e:
    bot_config = json.load(e)

class utility(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases='Ping', description='Shows the latency of the bot')
    async def _ping(self, ctx):
        await ctx.send(f'Latency :- `{round(self.bot.latency * 1000)} ms`')

    @commands.command(name='av', description='Shows the avatar of someone', aliases='avatar')
    async def _av(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
    
        embed = discord.Embed(color=bot_config['color']['default'], title=f"{member}'s avatar")
        embed.set_image(member.display_avatar_url)
        await ctx.send(embed=embed, reply=True)

    @commands.command(aliases='Embed', name='embed', description='Creates an embed, separate the title from the description with |')
    async def _embed(self, ctx, text):
        channel = ctx.channel

        try:
            title, description = text.split("|", 1)
            embed = discord.Embed(title=title, description=description, color=bot_config['color']['default'])
            await channel.send(embed=embed)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(utility(bot))