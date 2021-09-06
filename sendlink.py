import datetime

import discord
from discord.ext import commands
from discord import Colour,Embed,Member,utils,Forbidden,NotFound
from discord.ext.commands import has_permissions

class AutoMessagesSendSystem(commands.Cog):

    def __init__(self,bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message):
        message_content,*message_url = str(message.content).split('/')
        if len(message_url) >= 2:
            if message_url[1] == "discord.com" and message_url[2] == "channels":
                if int(message_url[3]) == int(message.guild.id):
                    text_channel = self.bot.get_channel(int(message_url[4]))
                    try:
                        msg = await text_channel.fetch_message(int(message_url[5]))
                    except NotFound:
                        pass
                    else:
                        if len(msg.embeds) >= 1:
                            msg_found = Embed(title=msg.embeds[0].title,description=msg.embeds[0].description)
                            for field in msg.embeds[0].fields:
                                msg_found.add_field(name=field.name,value=field.value)
                            msg_found.set_footer(text=f"Publié sur {text_channel.name} | Message posté le {msg.created_at}",icon_url=msg.guild.icon_url)
                        else:
                            msg_found = Embed(colour=discord.Colour.gold())
                            msg_found.add_field(name=f"Message posté le {msg.created_at}",value=msg.content)
                            msg_found.set_footer(text=f"Publié sur {text_channel.name}",icon_url=msg.guild.icon_url)
                        msg_found.set_author(name=msg.author.name,icon_url=msg.author.avatar_url)
                        await message.channel.send(embed=msg_found)
