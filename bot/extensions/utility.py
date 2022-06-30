import hikari
import lightbulb
import json

plugin = lightbulb.Plugin("utility")
ephemeral = hikari.MessageFlag.EPHEMERAL

with open("./config/stuff.json") as e:
    bot_config = json.load(e)

@plugin.command()
@lightbulb.command("ping", "Check the latency of the bot")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def _ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Latency: `{ctx.bot.heartbeat_latency*1000:.2f} ms`", reply=True)

@plugin.command()
@lightbulb.option("member", "the member to show", type=hikari.Member, required=False, default=None)
@lightbulb.command("avatar", "shows the members display avatar", aliases=["av", "avatar"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def _av(ctx: lightbulb.Context) -> None:
    member = ctx.options.member
    if member == None:
        member = ctx.event.message.member
    
    embed = hikari.Embed(color=bot_config['color']['default'], title=f"{member}'s avatar")
    embed.set_image(member.display_avatar_url)
    await ctx.respond(embed=embed, reply=True)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)