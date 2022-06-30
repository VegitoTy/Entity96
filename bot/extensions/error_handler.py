import discord
from discord import app_commands
import json
from discord.ext import commands

error_emote = "<:1326_cross:991726586590150737>"
ephemeral = discord.MessageFlags.ephemeral

with open("./config/stuff.json") as f:
    bot_config = json.load(f)

class error_handler(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener('on_command_error')
    async def errorhandler(self, ctx:commands.Context, exception):
        sus = False

        if isinstance(exception, commands.CommandInvokeError):
          description = f"> Something went wrong during invocation of command `{ctx.command}`."
          sus = True

        if isinstance(exception, commands.CommandNotFound):
            return
        
        exception = exception.__cause__ or exception

        if isinstance(exception, commands.NotOwner):
            description = f"> You are not the owner of this bot."
        elif isinstance(exception, commands.CommandOnCooldown):
            description = f"> This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds."
        elif isinstance(exception, commands.errors.CheckFailure):
            description = f"> You do not have the right permissions to use this command"
            return
        elif isinstance(exception, commands.errors.MissingRequiredArgument):
            args = ""
            for arg in exception.missing_options:
                args = args + f"`{arg.name}`, "
            args = args[:-2]
            description = f"> Missing required argument(s): {args}"
        elif isinstance(exception, TypeError):
            description = "> Invalid option type"
        else:
            description = f"!! There was a error with this command\n{exception}"
            sus = True

        embed = discord.Embed(title=f"{error_emote} Error", description=description, color=0x3498db)

        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.send(embed=embed)
        
        if sus == True:
            raise exception

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        error_handler(bot),
        guilds = [discord.Object(id = 837616575976177727)]
    )