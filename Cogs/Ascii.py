import asyncio
import discord
import random
from   discord.ext import commands
from   Cogs import Settings
from   Cogs import DisplayName
from   Cogs import Nullify
from   Cogs import DL
import urllib

def setup(bot):
    # Add the bot
    bot.add_cog(Ascii(bot))
    
class Ascii(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    @commands.command(pass_context=True, no_pm=True)
    async def ascii(self, ctx, *, text : str = None):
        """Beautify text (font list dapat dilihat di: http://artii.herokuapp.com/fonts_list)."""

        if text == None:
            em = discord.Embed(color = 0XFF8C00,
                               description = "> **Panduan penggunaan**\n"
                                            "> `{}ascii [font (optional)] [text]`\n> \n"
                                             "> Font list dapat dilihat dibawah ini\n"
                                             "> http://artii.herokuapp.com/fonts_list"
                                             .format(ctx.prefix))
            em.set_author(name = "ASCII", url = "http://artii.herokuapp.com/fonts_list", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return

        # Get list of fonts
        fonturl = "http://artii.herokuapp.com/fonts_list"
        response = await DL.async_text(fonturl)
        fonts = response.split()

        font = None
        # Split text by space - and see if the first word is a font
        parts = text.split()
        if len(parts) > 1:
            # We have enough entries for a font
            if parts[0] in fonts:
                # We got a font!
                font = parts[0]
                text = ' '.join(parts[1:])
    
        url = "http://artii.herokuapp.com/make?{}".format(urllib.parse.urlencode({'text':text}))
        if font:
            url += '&font={}'.format(font)
        response = await DL.async_text(url)
        em = discord.Embed(color = 0XFF8C00, description = "```Markup\n{}```".format(response))
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.channel.send(embed = em)
