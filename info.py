from datetime import datetime
from typing import Optional
from discord import Embed, Member
import discord
from discord.errors import ClientException
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command


class Info(Cog):
    def __init__(self, client):
        self.client = client

    @command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        embed = Embed(title="User information",
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=target.avatar_url)

        fields = [("📁|Name", str(target), True),
                  ("💳|ID", target.id, True),
                  ("🤖|Bot?", target.bot, True),
                  ("✨|Meilleur role", target.top_role.mention, True),
                  ("🗽|Status", str(target.status).title(), True),
                  ("🥋|Activité",
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}",
                   True),
                  ("🛠️|Crée le", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("📰|Rejoins le", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("🌟|Boosted", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    async def server_info(self, ctx):
        embed = Embed(title="Serveur information", colour=discord.Colour.gold(), timestamp=datetime.utcnow())
        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("💳|ID", ctx.guild.id, True),
                  ("👑|Créateur", ctx.guild.owner, True),
                  ("🌎|Region", ctx.guild.region, True),
                  ("🗓|Crée le", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("👑|Membres", len(ctx.guild.members), True),
                  ("🙋🏽‍♂||Humains", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("🤖|Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("⛔|Membres bans", len(await ctx.guild.bans()), True),
                  ("🗂|Status", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  # ("En ligne", f"🟢 {statuses[0]}", True),
                  # ("Inactif", f"🟠 {statuses[1]}", True),
                  # ("Ne pas déranger", f"🔴 {statuses[2]}", True),
                  # ("Hors ligne", f"⚪ {statuses[3]}", True),
                  ("⌨|Salons textuels", len(ctx.guild.text_channels), True),
                  ("🎤|Salon vocal", len(ctx.guild.voice_channels), True),
                  ("📚|Categories", len(ctx.guild.categories), True),
                  ("📍|Roles", len(ctx.guild.roles), True),
                  ("🎫|Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

