import os
import hikari
import lightbulb
import miru
import pathlib
from bot import extensions
import json
from lightbulb.ext import tasks

with open('./stuff/secret') as f:
    _token = f.read().strip()

with open('./config/stuff.json') as e:
    bot_config = json.load(e)

bot = lightbulb.BotApp(
    token=_token,
    prefix=lightbulb.when_mentioned_or(bot_config["bot"]["prefix"]),
    default_enabled_guilds=bot_config["bot"]["default_guild"],
    owner_ids=bot_config["bot"]["owner_ids"],
    ignore_bots=True,
    intents=hikari.Intents.ALL
)

@bot.listen(hikari.StartedEvent)
async def on_started(event : hikari.StartedEvent) -> None:
    channel = await bot.rest.fetch_channel(bot_config["logging"]["startup"])
    await channel.send("Bot has Started")

@bot.listen(hikari.StoppingEvent)
async def on_stop(event : hikari.StoppingEvent) -> None:
    channel = await bot.rest.fetch_channel(bot_config["logging"]["startup"])
    await channel.send("Bot has Stopped")

bot.load_extensions_from(pathlib.Path(os.path.realpath(extensions.__file__)).parent, must_exist=True)
bot.load_extensions("lightbulb.ext.filament.exts.superuser")
miru.load(bot)
tasks.load(bot)

@bot.command()
@lightbulb.option("extension", "The extension to reload", modifier=lightbulb.commands.base.OptionModifier(3))
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("reload", "reload a bots extension")
@lightbulb.implements(lightbulb.PrefixCommand)
async def _reload(ctx: lightbulb.Context) -> None:
    extension = ctx.options.extension
    try:
        ctx.bot.reload_extensions(f"bot.extensions.{extension}")
        embed = hikari.Embed(description=f"Reloaded extention {extension}", color=bot_config["color"]["default"])
    except Exception as e:
        embed = hikari.Embed(description=f"Reloading extention {extension} failed.\nError: {e}", color=bot_config["color"]["default"])
    await ctx.respond(embed=embed, reply=True)

@bot.command()
@lightbulb.option("extension", "The extension to load", modifier=lightbulb.commands.base.OptionModifier(3))
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("load", "load a bots extension")
@lightbulb.implements(lightbulb.PrefixCommand)
async def _load(ctx: lightbulb.Context) -> None:
    extension = ctx.options.extension
    try:
        ctx.bot.load_extensions(f"bot.extensions.{extension}")
        embed = hikari.Embed(description=f"Loaded extention {extension}", color=bot_config["color"]["default"])
    except Exception as e:
        embed = hikari.Embed(description=f"loading extention {extension} failed.\nError: {e}", color=bot_config["color"]["default"])
    await ctx.respond(embed=embed, reply=True)

@bot.command()
@lightbulb.option("extension", "The extension to load", modifier=lightbulb.commands.base.OptionModifier(3))
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("unload", "Unload a bots extension")
@lightbulb.implements(lightbulb.PrefixCommand)
async def _unload(ctx: lightbulb.Context) -> None:
    extension = ctx.options.extension
    try:
        ctx.bot.unload_extensions(f"bot.extensions.{extension}")
        embed = hikari.Embed(description=f"Unloaded extention {extension}", color=bot_config["color"]["default"])
    except Exception as e:
        embed = hikari.Embed(description=f"Unloading extention {extension} failed.\nError: {e}", color=bot_config["color"]["default"])
    await ctx.respond(embed=embed, reply=True)

bot.run(
    status=hikari.Status.DO_NOT_DISTURB,
    activity=hikari.Activity(
        name="Over TheSPACE",
        type=hikari.ActivityType.WATCHING,
    )
)