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

@plugin.command()
@lightbulb.option("text", "the content of the embed", required=True, modifier=lightbulb.commands.base.OptionModifier(3))
@lightbulb.option("channel", "the channel to send the embed to", type=hikari.GuildChannel, default=None, required=False)
@lightbulb.command("embed", "Creates an embed in the specified channel, separate the title from the description with |")
@lightbulb.implements(lightbulb.PrefixCommand)
async def _embed(ctx : lightbulb.Context) -> None:
    channel = ctx.options.channel
    text = ctx.options.text
    color = ctx.options.color
    
    if not channel:
        cid = ctx.event.message.channel_id
    else:
        cid = channel.id
    
    try:
        title, description = text.split("|", 1)
        embed = hikari.Embed(title=title, description=description, color=bot_config['color']['default'])
        await ctx.app.rest.create_message(cid, embed=embed)
        await ctx.event.message.add_reaction("✅")
    except:
        await ctx.event.message.add_reaction("❌")
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)