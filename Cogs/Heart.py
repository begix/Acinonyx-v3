import asyncio
import discord
import re
import random
from   discord.ext import commands
from   Cogs import DisplayName

def setup(bot):
    # Add the bot
    bot.add_cog(Heart(bot))


class Heart(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot
        # compile regex to look for i + hug or hug + me
        self.regex = re.compile(r"((.*?)\bi\b(.*?)\bhug\b(.*?))|((.*?)\bhug\b(.*?)\bme\b(.*?))")
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    async def message(self, message):
        # Check the message - and append a heart if a ping exists, but no command
        context = await self.bot.get_context(message)
        if context.command:
            return {}
        # Check for a mention
        bot_mentions = ["<@!{}>".format(self.bot.user.id), "<@{}>".format(self.bot.user.id)]
        react_list = []
        # Get our hug phrases
        matches = re.finditer(self.regex, message.content.lower())
        if len(list(matches)):
            react_list.append("🤗")
        for x in bot_mentions:
            if x in message.content:
                # We got a mention!
                emojis = ["<a:check:765458567985102848>",
                          "<a:angry_ping:770977833257533480>",
                          "<a:jelly_jump:770977977370017832",
                          "<a:Happydance:768057820834168852",
                          "<a:1488_poundcat:773150417315430430",
                          "<a:3774_Ping999:773150889174106112>",
                          "<a:2545_Kuma_RainbowHype:773151166523506699>",
                          "❤"]
                randEmojis = random.choice(emojis)
                react_list.append(randEmojis)
        # Return our reactions - if any
        if len(react_list):
            return { "Reaction" : react_list }

