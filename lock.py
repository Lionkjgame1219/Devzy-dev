import discord
from discord.ext import commands
import random
from discord import errors


from discord.ext.commands.errors import MissingPermissions

class Channels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"Le salon`{channel.name}` à bien été bloqué")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"Le salon`{channel.name}` à bien été bloqué")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"Le salon `{channel.name}` à bien été débloqué")

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
            await ctx.send(embed=embed)