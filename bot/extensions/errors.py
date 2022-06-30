import discord
from discord.ext import commands

error_emote = "<:1326_cross:991726586590150737>"
ephemeral = discord.MessageFlags.ephemeral

class error_handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener('on_command_error')
    async def errorhandler(self, ctx:commands.Context, exception):
        sus = False
        embed = discord.Embed(title=f"{error_emote} Error", color="FF0000")

        if isinstance(exception, commands.CommandInvokeError):
          embed.description = f"> Something went wrong during invocation of command `{ctx.command}`."
          sus = True

        if isinstance(exception, commands.CommandNotFound):
            return
        
        exception = exception.__cause__ or exception

        if isinstance(exception, commands.NotOwner):
            embed.description = f"> You are not the owner of this bot."
        elif isinstance(exception, commands.CommandOnCooldown):
            embed.description = f"> This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds."
        elif isinstance(exception, commands.errors.CheckFailure):
            embed.description = f"> You do not have the right permissions to use this command"
            return
        elif isinstance(exception, commands.errors.MissingRequiredArgument):
            args = ""
            for arg in exception.missing_options:
                args = args + f"`{arg.name}`, "
            args = args[:-2]
            embed.description = f"> Missing required argument(s): {args}"
        elif isinstance(exception, TypeError):
            embed.description = "> Invalid option type"
        else:
            embed.description = f"!! There was a error with this command\n{exception}"
            sus = True

        try:
            await ctx.send(embed=embed, flags=ephemeral, reply=True)
        except:
            try:
                await ctx.send(embed=embed, reply=True)
            except:
                await ctx.send(embed=embed)
        
        if sus == True:
            raise exception

def setup(bot):
    bot.add_cog(error_handler(bot))