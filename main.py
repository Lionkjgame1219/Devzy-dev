import discord
from discord import PermissionOverwrite
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, MissingPermissions
from index import create_voice_channel, get_category_by_name
from lock import Channels
from info import Info
import wikipedia
from typing import Optional
from googlesearch import search
import urllib.request
import re
from sendlink import AutoMessagesSendSystem
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
#from ticket import TicketSystem
client = commands.Bot(command_prefix='&', help_command=None, intents = discord.Intents.all())
#slash = SlashCommand(client, sync_commands=True)
client.add_cog(Channels(client))
client.add_cog(Info(client))
client.add_cog(AutoMessagesSendSystem(client))
#client.add_cog(TicketSystem(client))

@client.event
async def on_ready():
    activity = discord.Game(name="&help, v1.0.0", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("carré Chakal")


@client.event
async def on_message(message):
    if message.content == 'salut' or message.content == 'coucou' or message.content == 'bonsoir' or message.content == 'bonjour':
        await message.channel.send(f"{message.author.mention} salut ")

    if message.content == "dev du bot":
        embed = discord.Embed(title="||lion kj game667#7138||", colour=discord.Colour.green())
        await message.channel.send(embed=embed)

    if message.content == "prefix":
        embed = discord.Embed(title="Le prefix du bot est &", colour=discord.Colour.green())
        await message.channel.send(embed=embed)

    await client.process_commands(message)




@client.event
async def on_raw_reaction_add(payload):
    message = 874622139926478849

    if message == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '✅':
            role = discord.utils.get(guild.roles, name="Membre")

        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    message = 874622139926478849
    if message == payload.message_id:
        guild = await(client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '✅':
            role = discord.utils.get(guild.roles, name="Membre")
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)

        else:
            print("Member not found")

@client.event
async def on_member_join(member):
    embed = discord.Embed(title=f"Bienvenu {member} n'hésite pas à beaucoup parler dans le serveur!", colour=discord.Colour.green())
    await member.send(embed=embed)

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if not before.channel:
        print(f"{member.name} joined {after.channel.name}")

    if before.channel and not after.channel:
        print("User left channel")

    if before.channel and after.channel:
        if before.channel.id != after.channel.id:
            print("User switched voice channel")

        else:
            print("Something else happened")
            if member.voice.stream:
                print("User start stream")

            elif member.voice.mute:
                print("mute")

            elif member.voice.deaf:
                print("User deafened")
            else:
                print("We are here")

    # if after.channel is not None:
    #    if after.channel.name == "salon-privé":
    #        channel = await create_voice_channel(after.channel.guild, f'🔒{member.name}'.lower(), category_name="salonprivé", user_limit=after.channel.user_limit)
    #        await channel.set_permissions(member, connect=True, speak=True)

    #        if channel is not None:
    #            await member.move_to(channel)

    # if before.channel is not None:
    #    if before.channel.category.id == get_category_by_name(before.channel.guild, "salonprivé").id:
    #        if len(before.channel.members) == 0:
    #            await before.channel.delete()

    if after.channel is not None:
        if "🎵" in after.channel.name:
            channel = await create_voice_channel(after.channel.guild, f'🔓{member.name}'.lower(), category_name="🎶| salons-temporaire", user_limit=after.channel.user_limit)
            await channel.set_permissions(member, connect=True, speak=True)

            if channel is not None:
                await member.move_to(channel)

    if before.channel is not None:
        if before.channel.category.id == get_category_by_name(before.channel.guild, "🎶| salons-temporaire").id:
            if len(before.channel.members) == 0:
                await before.channel.delete()


@client.command()
async def say(ctx, *name):
    await ctx.message.delete()
    name = " ".join(name)
    await ctx.send(name)

@client.command()
async def ping(ctx: commands.Context):
    ping = round(client.latency * 1000)

    if ping > 200:
        embed = discord.Embed(title="Ping latency", description=f' 🔴 pong! {ping}ms', colour=discord.Colour.red())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! ", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
    elif ping <= 200:
        embed = discord.Embed(title="Ping latency", description=f' 🟠 pong! {ping}ms', colour=discord.Colour.orange())
        embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous!", icon_url=client.user.avatar_url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    elif ping >= 0:
        embed = discord.Embed(title="Ping latency", description=f' 🟢 pong! {ping}ms', colour=discord.Colour.green())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! ",
                         icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def bl(ctx, member: discord.Member, channel: discord.TextChannel):
    def set_permissions():
        perms = discord.PermissionOverwrite()
        perms.read_messages = False
        return perms

    await channel.set_permissions(member, overwrite=set_permissions())
    embed = discord.Embed(title=f"Le membre {member} a bien été blacklist du salons {channel.name} ✅")
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def wl(ctx, member: discord.Member, channel: discord.TextChannel):
    def set_permissions():
        perms = discord.PermissionOverwrite()
        perms.read_messages = True
        return perms

    await channel.set_permissions(member, overwrite=set_permissions())
    embed = discord.Embed(title=f"Le membre {member } a bien été whitelist du salons {channel.name} ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@client.command()
async def idmember(ctx, member: discord.Member):
    await ctx.send(f"L'identifiant de `{member}` est `{member.id}`")

@client.command()
@commands.has_permissions(administrator = True)
async def addrole(ctx, role: discord.Role, member: discord.Member=None):
    if member is not None:
        await member.add_roles(role)
        embed = discord.Embed(title=f"vous avez attribuer le role {role} au membre {member} ✅", colour=discord.Colour.green())
        await ctx.send(embed=embed)

    else:
        await ctx.message.author.add_roles(role)
        embed = discord.Embed(title=f"vous vous êtes attribuer le role {role} ✅", colour=discord.Colour.green())
        await ctx.send(embed=embed)


@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $addrole <@role ou id du role>")
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx, role: discord.Role, member: discord.Member=None):
    if member is not None:
        await member.remove_roles(role)
        embed = discord.Embed(title=f"Le role {role} a été enlever pour le membre {member} ✅", colour=discord.Colour.green())
        await ctx.send(embed=embed)

    else:
        await ctx.message.author.remove_roles(role)
        embed = discord.Embed(title=f"vous vous êtes enlever le role {role} ✅", colour=discord.Colour.green())
        await ctx.send(embed=embed)

@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $removerole <mention du membre ou id du membre> <id du role ou @<nom du role> ")
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def create_textchannel(ctx, *name):
    guild = ctx.guild
    name = " ".join(name)
    await guild.create_text_channel(f"{name}")
    embed = discord.Embed(title=f"Le salons {name} a bien été créer ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)


@create_textchannel.error
async def createtext_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $create_textchannel <nom du salons>")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def create_textprivate(ctx, *name):
    guild = ctx.guild
    name = " ".join(name)
    overwrite = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel(f"{name}", overwrites=overwrite)
    embed = discord.Embed(title=f"Le salons {name} a bien été créer ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)

"""
async def create_voice_channel(guild, channel_name, user_limit=None):
    
    Creates a new channel in the category "Game"
    
    await guild.create_voice_channel(channel_name, category=category, user_limit=user_limit)

    channel = get_channel_by_name(guild, channel_name)
    # await channel.set_permission(member, connect=True, speak=True)
    return channel
"""

@create_textprivate.error
async def text_private(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $create_textprivate <nom du salons>")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def create_voicechannel(ctx, *name):
    guild = ctx.guild
    name = " ".join(name)
    await guild.create_voice_channel(f"{name}")
    embed = discord.Embed(title=f"Le salons {name} a bien été créer ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@create_voicechannel.error
async def createvoice_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $create_voicechannel <nom du salons vocal>")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def delete_channel(ctx, channel_name):
    guild = ctx.guild
    # check if the channel exists
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    # if the channel exists
    if existing_channel is not None:
        await existing_channel.delete()
        embed = discord.Embed(title=f"Le salons {channel_name} a bien été supprimer ✅", colour=discord.Colour.green())
        await ctx.send(embed=embed)
    # if the channel does not exist, inform the user
    else:
        embed = discord.Embed(title=f"Le salons {channel_name} n'existe pas ❌", colour=discord.Colour.red())
        await ctx.send(embed=embed)

@delete_channel.error
async def deletechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $delete_channel #channel")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def create_role(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Le nom du role')
    title = await client.wait_for('message', check=check)

    await ctx.send('Voulez vous que le role aie les permissions dadministration?')
    kickperm = await client.wait_for('message', check=check)

    guild = ctx.guild
    role = await guild.create_role(name=title.content, colour=discord.Colour.green())

    if kickperm.content == "oui":
        permissions = discord.Permissions()
        permissions.update(administrator=True)
        await role.edit(reason=None, permissions=permissions)
    else:
        await ctx.send("pas de permissions ajoutée")
    embed = discord.Embed(title=f"Le role {role} a bien été créer ✅", colour=discord.Colour(0x36fd00))
    await ctx.send(embed=embed)

@create_role.error
async def createrole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def embed(ctx, channel: discord.TextChannel):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send("Mettez un titre")
    title = await client.wait_for('message', check=check)

    await ctx.send("Mettez une description")
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content, colour=discord.Colour.green())
    msg = await channel.send(embed=embed)

@embed.error
async def embed_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $embed #channel")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def clear(ctx, amount=5):
    embed = discord.Embed(title=f"{amount} messages on été supprimé ✅", colour=discord.Colour.green(), delete_after=10)
    await ctx.send(embed=embed)
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $clear <nombre de message a supprimer>")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason="aucune raison"):
    server = ctx.guild
    await member.ban(reason=reason)
    embed = discord.Embed(title=f"{member} a été bannis || `{reason}` ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)
    en = discord.Embed(description=f"vous avez été bannis du serveur `{server.name}` || `{reason}`", colour=discord.Colour.red())
    await member.send(embed=en)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $ban <id ou pseudo> (raison)")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def unban(ctx, user):
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user)
            embed = discord.Embed(title=f"{user} a été débanni(e) ✅", colour=discord.Colour.green())
            await ctx.send(embed=embed)

            return
    embed = discord.Embed(title="Erreur unban", description="L'utilisateur n'as pas été trouver dans la liste des bans! <:warning:873482928720584747>", colour=discord.Colour.red())
    await ctx.send(embed=embed)


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $unban <pseudo ou id>")
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="aucune raison"):
    server = ctx.guild
    await member.kick(reason=reason)
    embed = discord.Embed(title=f"{member} a été kick || `{reason}` ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)
    en = discord.Embed(description=f"vous avez été kick du serveur `{server.name}` || `{reason}`", colour=discord.Colour.red())
    await member.send(embed=en)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $kick <id ou pseudo> (raison)")
        await ctx.send(embed=embed)



async def create_muted_role(ctx):
    mutedrole = await ctx.guild.create_role(name="Muted", permissions= discord.Permissions(send_messages = False, speak=False), reason = "Creation du role muted")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedrole, send_messages=False, speak=False)
    return mutedrole


async def getmutedrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await create_muted_role(ctx)


#commande mute
@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason="aucune raison"):
    mutedrole = await getmutedrole(ctx)
    await member.add_roles(mutedrole, reason=reason)
    embed = discord.Embed(title=f"{member} a été mute || `{reason}` ✅", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite $mute <id ou pseudo> (raison)")
        await ctx.send(embed=embed)

#unmute commande
@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, *, reason="aucune raison"):
    mutedRole = await getmutedrole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    embed = discord.Embed(title=f"{member} a été unmute ✅", colour=discord.Colour.green())

    await ctx.send(embed=embed)


#Unmute error
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>", description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)

    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite chakal/unmute <id ou pseudo> <reason>")
        await ctx.send(embed=embed)

@client.command()
async def nick(ctx, nick):
    await ctx.author.edit(nick=nick)
    embed = discord.Embed(title="Rename pseudo", colour=discord.Colour.green(), description=f"Votre pseudo à bien été modifié en `{nick}`.<:white_check_mark:873491327323602956>")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True)
async def rename(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f"Le membre `{member.name}` à été rename en `{nick}` ✅")


@rename.error
async def rename_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide",
                              description="Faite $rename <id du membre> <le nouveau pseudo>")
        await ctx.send(embed=embed)

    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="<:warning:873482928720584747>",
                              description="Vous n'avez pas le droit de faire cette commande")
        await ctx.send(embed=embed)


# channel: discord.VoiceChannel
@client.command()
async def config(ctx, *, new_name):
    await ctx.author.voice.channel.edit(name=new_name)
    embed = discord.Embed(title="Rename du salons vocal",
                          description=f"Le nom du salon vocal à bien été changé en `{new_name}`")
    await ctx.send(embed=embed)

@client.command()
async def public(ctx):
    guild = ctx.guild
    def set_permissions():
        perms = discord.PermissionOverwrite()
        perms.read_messages = True
        perms.connect = True
        return perms


    vocal_channel = ctx.author.voice.channel
    await vocal_channel.set_permissions(guild.default_role, overwrite=set_permissions())
    await ctx.send("Le salon a bien été rendu publique")

@client.command()
async def private(ctx):
    guild = ctx.guild
    def set_permissions():
        perms = discord.PermissionOverwrite()
        perms.read_messages = True
        perms.connect = False
        return perms

    vocal_channel = ctx.author.voice.channel
    await vocal_channel.set_permissions(guild.default_role, overwrite=set_permissions())
    await ctx.send("Le salon a bien été rendu privée")


@client.command()
async def whitelist(ctx, member: discord.Member):
    def set_permissions():
        perms = discord.PermissionOverwrite()
        perms.read_messages = True
        perms.connect = True
        return perms

    vocal_channel = ctx.author.voice.channel
    await vocal_channel.set_permissions(member, overwrite=set_permissions())
    await ctx.send("un membre a bien été whitelist ✅")


@client.command()
async def blacklist(ctx, member: discord.Member):
    def set_permissions():
        perms = discord.PermissionOverwrite()
        perms.read_messages = True
        perms.connect = False
        return perms

    vocal_channel = ctx.author.voice.channel
    await vocal_channel.set_permissions(member, overwrite=set_permissions())
    await ctx.send("Le membre a bien été blacklist ✅")



@client.command()
async def avatar(ctx, member: discord.Member=None):
    if member is not None:
        embed = discord.Embed(colour=discord.Colour.teal())
        embed.set_image(url="{}".format(member.avatar_url))
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(colour=discord.Colour.teal())
        embed.set_image(url="{}".format(ctx.message.author.avatar_url))
        await ctx.send(embed=embed)

@client.command()
async def prefix(ctx):
    await ctx.send("Mon prefix est $")

@client.command()
async def lien(ctx):
    await ctx.send("Voici mon lien d'invitation: https://discord.com/api/oauth2/authorize?client_id=872038536336007198&permissions=8&scope=bot%20applications.commands")

@client.command()
async def lien_server(ctx):
    member = ctx.author
    await member.send("Voici mon serveur de developemment: https://discord.gg/DRTfXQjU et mon serveur fun: https://discord.gg/6tRZ4fZw")


@client.command()
async def wiki(ctx, *, query):
    await ctx.message.delete()
    for channel in ctx.guild.channels:
        if 'wiki-result' in channel.name:
            wikipedia.set_lang("fr")
            try:
                embed = discord.Embed(title=f"Wiki search: {query}", description=wikipedia.summary(query)+f'\ndemander par {ctx.message.author.mention}', colour = discord.Colour.purple())
                await channel.send(embed=embed)
            except Exception:
                for new_query in wikipedia.search(query):
                    try:
                        embed = discord.Embed(title=f"Wiki search: {query}", description=wikipedia.summary(new_query)+f'\ndemander par{ctx.message.author.mention}', colour = discord.Colour.purple())
                        await channel.send(embed=embed)
                    except Exception:
                        pass
            await ctx.send(f"Aller dans le salon <#{channel.id}> pour voir les réponse trouver {ctx.message.author.mention}✅")

@wiki.error
async def wiki_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite ?wiki <recherche>", colour=discord.Colour.gold())
        await ctx.send(embed=embed)

@client.command()
async def google(ctx, *,recherche):
    await ctx.message.delete()
    search_query= recherche
    for i in search(search_query, tld='com', lang='fr', num=1, stop=1, pause=2.0):
        await ctx.send(i)
        await ctx.send(f"Voici votre commande google {ctx.message.author.mention}")

@google.error
async def google_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite ?google <recherche>", colour=discord.Colour.gold())
        await ctx.send(embed=embed)

@client.command()
async def youtube(ctx, search):
    await ctx.message.delete()
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    await ctx.send("https://www.youtube.com/watch?v="+ video_ids[0])
    await ctx.send(f"Voici votre commande youtube {ctx.message.author.mention}")


@youtube.error
async def youtube_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title="<:warning:873482928720584747> Argument non valide", description="Faite ?youtube <recherche> si vous avez une recherche qui contient des espaces, faites ?youtube <recherche+recherche>", colour=discord.Colour.gold())
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def nombre_de_membre(ctx):
    for member in ctx.guild.members:
        embed = discord.Embed(title=f"{member}", colour=discord.Colour.green())
        await ctx.send(embed=embed)



@client.command()
async def help(ctx):
    embed = discord.Embed(title="&help", description="💎admin💎\n⚔️modération⚔️\n💈communauté💈\n⚙️all⚙️\n🎵commande-vocal🎵\n🗞wikipédia\ncancel pour terminer la commande||ne mettez les emojis devant mettez juste le nom {}=facultatif||",colour=discord.Colour.blurple())
    await ctx.send(embed=embed)
    while True:
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        categorie = await client.wait_for('message', check=check)

        if categorie.content == 'admin' or categorie.content == 'administrateur':
            embedd = discord.Embed(title="💎admin💎", colour=discord.Colour.blue(), description="Faut avoir imperativement la permission d'administrateur")
            embedd.add_field(name="`create_textchannel <nom du salons>`", value="permet de créer des salons textuel", inline=False)
            embedd.add_field(name="`create_textprivate <nom du salons>`", value="permet de créer des salons textuel privée", inline=False)
            embedd.add_field(name="`create_voicechannel <nom du salons>`", value="permet de créer des salons vocal", inline=False)
            embedd.add_field(name="`delete_channel <nom du salons>`", value="permet de supprimer des salons textuel&vocal", inline=False)
            embedd.add_field(name="`addrole {member} <@role ou id du role>`", value="permet de se donner un role", inline=False)
            embedd.add_field(name="`removerole {mention ou id du member} <@role ou id du role>`", value="permet d'enlever un role", inline=False)
            embedd.add_field(name="`create_role`", value="permet de creer un role", inline=False)
            embedd.add_field(name="`embed <salons ou le poster>`", value="permet de creer un embed <commande en developpement>", inline=False)
            embedd.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embedd.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous!", icon_url = client.user.avatar_url)
            await ctx.send(embed=embedd)

        if categorie.content == 'modération' or categorie.content == 'modo':
            embed = discord.Embed(title="⚔️modération⚔️", colour=discord.Colour.purple(), description="Faut avoir imperativement la permission de kick des membres")
            embed.add_field(name="`ban <mention du membre ou id> {reason}`", value='ban des membres', inline=False)
            embed.add_field(name="`mute <mention du membre ou id> {reason}`", value="Enleve les permissions de parler dans tout les salons", inline=False)
            embed.add_field(name='`kick <mention du membre ou id> {reason}`', value="expulse des membres", inline=False)
            embed.add_field(name="`clear <nombre de message>`", value="permet de supprimer un certain nombre de messages", inline=False)
            embed.add_field(name="`lock`", value="Permet de bloquer un salons refaite la même commande pour débloquer", inline=False)
            embed.add_field(name="`rename <membre mention ou id> <nouveau pseudo>`", value="permet de renommer un membre")
            embed.add_field(name="`bl <mention du membre ou id du membre>`", value="Permet d'enlever la permssions de voir le salon à un membre", inline=False)
            embed.add_field(name="`wl <mention du membre ou id du membre>`", value="Permet de d'ajouter la permssions de voir le salon à un membre", inline=False)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! ", icon_url = client.user.avatar_url)
            await ctx.send(embed=embed)

        if categorie.content == 'communauté' or categorie.content == 'commu':
            embed = discord.Embed(title="💈communauté💈", colour=discord.Colour.purple())
            embed.add_field(name="`lien_server`", value="vous donne les liens des serveurs ou le créateur se trouve", inline=False)
            embed.add_field(name="`lien`", value="vous donne le lien d'invitation du bot pour l'ajouter à votre serveur", inline=False)
            embed.add_field(name="`say <texte>`", value="Recopie le texte et l'affiche", inline=False)
            embed.add_field(name="`ping`", value="affiche la latence de votre connexion", inline=False)
            embed.add_field(name="`nick <nouveau pseudo>`", value="Permet de se renommer sur le serveur", inline=False)
            embed.add_field(name="`serverinfo, gi, si`", value="Permet de voir les informations du serveur", inline=False)
            embed.add_field(name="`ui, mi, memberinfo, userinfo`", value="Permet de voir les informations d'un membre ou de vous", inline=False)
            embed.add_field(name="`avatar <mention de quelqu'un facultatif> `", value="Permet de voir votre photo de profil", inline=False)
            embed.add_field(name="`wiki <recherche>`", value="Permet de faire des recherches wikipedia", inline=False)
            embed.add_field(name="`google <recherche>`", value="Permet de faire des recherches google", inline=False)
            embed.add_field(name="`youtube <recherche>`", value="Permet de faire des recherches youtube au lieux de mettre des espaces remplacer ça par des +", inline=False)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! ", icon_url = client.user.avatar_url)
            await ctx.send(embed=embed)

        if categorie.content == 'commande-vocal':
            embed = discord.Embed(title="🎵commande-vocal🎵", colour=discord.Colour.random())
            embed.add_field(name="`public`", value="rend votre salon publique", inline=False)
            embed.add_field(name="`private`", value="rend votre salon privé", inline=False)
            embed.add_field(name="`whitelist <mention de la personne à whitelist>`", value="rend votre salon accessible pour un membre précis", inline=False)
            embed.add_field(name="`blacklist <mention de la personne à blacklist>`", value="rend votre salon inaccessible pour un membre précis même si votre salon est en publique", inline=False)
            embed.add_field(name="`config <name>`", value="modifie le nom de votre salons vocal", inline=False)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(
                text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous!",
                icon_url=client.user.avatar_url)
            await ctx.send(embed=embed)



        if categorie.content == 'wiki' or categorie.content == 'wikipédia' or categorie.content == 'wikipedia':
            embed = discord.Embed(title="Voulez-vous activer les recherches wikipedia?", description="si vous voulez activer les recherches wikipédia vous devrez créer un salons qui aura comme nom `wiki-result` vous pourrez le modifier mettre des emojis mais faut qu'il y est strictement le nom wiki-result et voila faite $wiki <recherche>", colour = discord.Colour.green())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! si vous recontrez un problème avec le bot veuillez contacter `lion kj game667` sur discord!", icon_url = client.user.avatar_url)
            await ctx.send(embed=embed)

        if categorie.content == 'all':
            member = ctx.author
            embedd = discord.Embed(title="💎admin💎", colour=discord.Colour.blue(), description="Faut avoir imperativement la permission d'administrateur")
            embedd.add_field(name="`create_textchannel <nom du salons>`", value="permet de créer des salons textuel", inline=False)
            embedd.add_field(name="`create_textprivate <nom du salons>`", value="permet de créer des salons textuel privée", inline=False)
            embedd.add_field(name="`create_voicechannel <nom du salons>`", value="permet de créer des salons vocal", inline=False)
            embedd.add_field(name="`delete_channel <nom du salons>`", value="permet de supprimer des salons textuel&vocal", inline=False)
            embedd.add_field(name="`addrole {member id ou mention} <@role ou id du role>`", value="permet de se donner un role", inline=False)
            embedd.add_field(name="`removerole {member id ou mention} <@role ou id du role>`", value="permet d'enlever un role", inline=False)
            embedd.add_field(name="`create_role`", value="permet de creer un role", inline=False)
            embedd.add_field(name="`embed <salons ou le poster>`", value="permet de creer un embed <commande en developpement>", inline=False)
            embedd.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embedd.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous!", icon_url = client.user.avatar_url)
            await member.send(embed=embedd)
            embed = discord.Embed(title="⚔️modération⚔️", colour=discord.Colour.purple(), description="Faut avoir imperativement les permissions de kick des membre")
            embed.add_field(name="`ban <mention du membre ou id> (reason)`", value='ban des membres', inline=False)
            embed.add_field(name="`mute <mention du membre ou id> (reason)`", value="Enleve les permissions de parler dans tout les salons", inline=False)
            embed.add_field(name='`kick <mention du membre ou id> (reason)`', value="expulse des membres", inline=False)
            embed.add_field(name="`clear <nombre de message>`", value="permet de supprimer un certain nombre de messages", inline=False)
            embed.add_field(name="`lock`", value="Permet de bloquer un salons refaite la même commande pour débloquer", inline=False)
            embed.add_field(name="`bl <mention du membre ou id du membre>`", value="Permet d'enlever la permssions de voir le salon à un membre", inline=False)
            embed.add_field(name="`wl <mention du membre ou id du membre>`", value="Permet de d'ajouter la permssions de voir le salon à un membre", inline=False)
            embed.add_field(name="`rename <membre mention ou id> <nouveau pseudo>`", value="permet de renommer un membre", inline=False)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! ", icon_url = client.user.avatar_url)
            await member.send(embed=embed)
            embeddd = discord.Embed(title="💈communauté💈", colour=discord.Colour.purple())
            embeddd.add_field(name="`say <texte>`", value="Recopie le texte et l'affiche", inline=False)
            embeddd.add_field(name="`ping`", value="affiche la latence de votre connexion", inline=False)
            embeddd.add_field(name="`ticket`", value="créer un ticket", inline=False)
            embeddd.add_field(name="`nick <nouveau pseudo>`", value="Permet de se renommer sur le serveur", inline=False)
            embeddd.add_field(name="`serverinfo, gi, si`", value="Permet de voir les informations du serveur", inline=False)
            embeddd.add_field(name="`ui, mi, memberinfo, userinfo`", value="Permet de voir les informations d'un membre ou de vous", inline=False)
            embeddd.add_field(name="`avatar <mention de quelqu'un facultatif> `", value="Permet de voir votre photo de profil", inline=False)
            embeddd.add_field(name="`wiki <recherche>`", value="Permet de faire des recherches wikipedia", inline=False)
            embeddd.add_field(name="`google <recherche>`", value="Permet de faire des recherches google", inline=False)
            embeddd.add_field(name="`youtube <recherche>`", value="Permet de faire des recherches youtube au lieux de mettre des espaces remplacer ça par des +", inline=False)
            embeddd.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embeddd.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous! ", icon_url = client.user.avatar_url)
            await member.send(embed=embeddd)
            embed2 = discord.Embed(title="🎵commande-vocal🎵", colour=discord.Colour.random())
            embed2.add_field(name="`public`", value="rend votre salon publique", inline=False)
            embed2.add_field(name="`private`", value="rend votre salon privé", inline=False)
            embed2.add_field(name="`whitelist <mention de la personne à whitelist>`", value="rend votre salon accessible pour un membre précis", inline=False)
            embed2.add_field(name="`blacklist <mention de la personne à blacklist>`", value="rend votre salon inaccessible pour un membre précis même si votre salon est en publique", inline=False)
            embed2.add_field(name="`config <name>`", value="modifie le nom de votre salons vocal", inline=False)
            embed2.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed2.set_footer(text=f"Votre serviteur: {client.user.name}, toujours disponible pour vous!", icon_url=client.user.avatar_url)
            await member.send(embed=embed2)


        if categorie.content == 'cancel':
            await ctx.send("commande terminer")
            break



