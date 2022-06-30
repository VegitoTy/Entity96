import hikari
import lightbulb

plugin = lightbulb.Plugin("errorhandler")
ephemeral = hikari.MessageFlag.EPHEMERAL

error_sign = "<:1326_cross:991726586590150737>"

@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    sus = False
    embed = hikari.Embed(title=f"{error_sign} Error", color="FF0000")
    
    if isinstance(event.exception, lightbulb.errors.CommandNotFound):
        return
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        embed.description = f"> Something went wrong during the usage of command `{event.context.command.name}`."
        sus = True
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.NotOwner):
        embed.description = f"-> You are not the owner of this bot."
        return
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        embed.description = f"-> This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds."
    elif isinstance(exception, lightbulb.errors.CheckFailure):
        embed.description = f"-> You do not have the right permissions to use this command"
        return
    elif isinstance(exception, lightbulb.errors.NotEnoughArguments):
        args = ""
        for arg in exception.missing_options:
            args = args + f"`{arg.name}`, "
        args = args[:-2]
        embed.description = f"-> Missing required argument(s): {args}"
    else:
        embed.description = f"!! There was a error with this command\n{exception}"
        sus = True
    
    try:
        await event.context.respond(embed=embed, flags=ephemeral, reply=True)
    except:
        try:
            await event.context.respond(embed=embed, reply=True)
        except:
            await event.context.respond(embed=embed)
    
    if sus:
        raise exception

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)