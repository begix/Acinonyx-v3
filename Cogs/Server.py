import asyncio, discord, os, re
from   datetime import datetime
from   discord.ext import commands
from   Cogs import Utils, Message, PCPP

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Server(bot, settings))

# This module sets/gets some server info

class Server(commands.Cog):

    # Init with the bot reference, and a reference to the settings var and xp var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        # Regex for extracting urls from strings
        self.regex = re.compile(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    async def message(self, message):
        if not type(message.channel) is discord.TextChannel:
            return { "Ignore" : False, "Delete" : False }
        # Make sure we're not already in a parts transaction
        if self.settings.getGlobalUserStat(message.author, 'HWActive'):
            return { "Ignore" : False, "Delete" : False }
        # Check if we're attempting to run the pcpp command
        the_prefix = await self.bot.command_prefix(self.bot, message)
        if message.content.startswith(the_prefix):
            # Running a command - return
            return { "Ignore" : False, "Delete" : False }
        # Check if we have a pcpartpicker link
        matches = re.finditer(self.regex, message.content)
        pcpplink = None
        for match in matches:
            if 'pcpartpicker.com' in match.group(0).lower():
                pcpplink = match.group(0)
        if not pcpplink:
            # Didn't find any
            return { "Ignore" : False, "Delete" : False }
        autopcpp = self.settings.getServerStat(message.guild, "AutoPCPP")
        if autopcpp == None:
            return { "Ignore" : False, "Delete" : False }
        ret = await PCPP.getMarkdown(pcpplink, autopcpp)
        return { "Ignore" : False, "Delete" : False, "Respond" : ret }

    # @commands.command(pass_context=True)
    # async def setprefix(self, ctx, *, prefix : str = None):
    #     """Mengatur prefix bot ini dalam server mu (admin/owner-server only).
    #     Mengetik command ini tanpa memasukan prefix akan menghapus costum prefix
    #     menjadi default `acx `"""
    #     isOwner = self.settings.isOwner(ctx.author)
    #     if not await Utils.is_bot_admin_reply(ctx): return
    #     # We're admin
    #     if not prefix:
    #         self.settings.setServerStat(ctx.guild, "Prefix", None)
    #         msg = 'Custom server prefix telah *dihapus*.'
    #     elif prefix in ['@everyone','@here']:
    #         return await ctx.send("Bagus, pintar sekali..!\njadi lebih mudah dan simpel..\n**PAKAI PREFIX LAIN!**")
    #     elif prefix in ['acx ']:
    #         self.settings.setServerStat(ctx.guild, "Prefix", prefix)
    #         msg = 'Custom server prefix menjadi: `{}`'.format(prefix)
    #     elif len(prefix) > 3:
    #         return await ctx.send("┐(￣ヘ￣;)┌\nprefix tidak dapat lebih dari 3, kecuali default!")
    #     else:
    #         self.settings.setServerStat(ctx.guild, "Prefix", prefix)
    #         msg = 'Custom server prefix menjadi: `{}`'.format(prefix)
    #     em = discord.Embed(color = 0XFF8C00, description = msg)
    #     em.set_footer(text = "{}".format(ctx.author))
    #     await ctx.send(embed = em)

    # @commands.command(pass_context=True, aliases=['o-setprefix'])
    # async def setprefixowner(self, ctx, *, prefix : str = None):
    #     """Mengatur prefix bot ini dalam server mu (owner-only)."""
    #     isOwner = self.settings.isOwner(ctx.author)
    #     if isOwner == False:
    #         return
    #     # We're admin
    #     if not prefix:
    #         self.settings.setServerStat(ctx.guild, "Prefix", None)
    #         msg = 'Custom server prefix telah *dihapus*.'
    #     elif prefix in ['@everyone','@here']:
    #         return await ctx.send("Bagus, pintar sekali..!\njadi lebih mudah dan simpel..\n**PAKAI PREFIX LAIN!**")
    #     elif prefix in ['acx ']:
    #         self.settings.setServerStat(ctx.guild, "Prefix", prefix)
    #         msg = 'Custom server prefix menjadi: `{}`'.format(prefix)
    #     elif len(prefix) > 3:
    #         return await ctx.send("┐(￣ヘ￣;)┌\nprefix tidak dapat lebih dari 3, kecuali default!")
    #     else:
    #         self.settings.setServerStat(ctx.guild, "Prefix", prefix)
    #         msg = 'Custom server prefix menjadi: `{}`'.format(prefix)
    #     em = discord.Embed(color = 0XFF8C00, description = msg)
    #     em.set_footer(text = "{}".format(ctx.author))
    #     await ctx.send(embed = em)

    # @commands.command(pass_context=True)
    # async def getprefix(self, ctx):
    #     """Melihat prefix saat ini yang digunakan dalam server mu.
    #     Jika lupa,
    #     mention bot ini dan ketik `getprefix` untuk mendapatkan prefix diserver mu"""
    #     # Get the current prefix
    #     prefix = await self.bot.command_prefix(self.bot, ctx.message)
    #     prefixlist = ", ".join([x for x in prefix if not x == "<@!{}> ".format(self.bot.user.id)])
    #     msg = 'Prefix{} bot dalam server ini: {}'.format("" if len(prefix) > 1 else "",prefixlist)
    #     em = discord.Embed(color = 0XFF8C00, description = msg)
    #     em.set_footer(text = "{}".format(ctx.author))
    #     await ctx.send(embed = em)
    
    # @commands.command(pass_context=True)
    # async def autopcpp(self, ctx, *, setting : str = None):
    #   """Sets the bot's auto-pcpartpicker markdown if found in messages (admin-only). Setting can be normal, md, mdblock, bold, bolditalic, or nothing."""
    #   if not await Utils.is_admin_reply(ctx): return
    #   if setting == None:
    #       # Disabled
    #       self.settings.setServerStat(ctx.guild, "AutoPCPP", None)
    #       msg = 'Auto pcpartpicker *disabled*.'
    #   elif setting.lower() == "normal":
    #       self.settings.setServerStat(ctx.guild, "AutoPCPP", "normal")
    #       msg = 'Auto pcpartpicker set to *Normal*.'
    #   elif setting.lower() == "md":
    #       self.settings.setServerStat(ctx.guild, "AutoPCPP", "md")
    #       msg = 'Auto pcpartpicker set to *Markdown*.'
    #   elif setting.lower() == "mdblock":
    #       self.settings.setServerStat(ctx.guild, "AutoPCPP", "mdblock")
    #       msg = 'Auto pcpartpicker set to *Markdown Block*.'
    #   elif setting.lower() == "bold":
    #       self.settings.setServerStat(ctx.guild, "AutoPCPP", "bold")
    #       msg = 'Auto pcpartpicker set to *Bold*.'
    #   elif setting.lower() == "bolditalic":
    #       self.settings.setServerStat(ctx.guild, "AutoPCPP", "bolditalic")
    #       msg = 'Auto pcpartpicker set to *Bold Italics*.'
    #   else:
    #       msg = "That's not one of the options."
    #   await ctx.send(msg)

    # @commands.command(pass_context=True)
    # async def setinfo(self, ctx, *, word : str = None):
    #   """Sets the server info (bot-admin only)."""
    #   if not await Utils.is_bot_admin_reply(ctx): return
    #   # We're admin
    #   word = None if not word else word
    #   self.settings.setServerStat(ctx.guild,"Info",word)
    #   msg = "Server info *{}*.".format("updated" if word else "removed")
    #   await ctx.send(msg)

    # @commands.command(pass_context=True)
    # async def info(self, ctx):
    #   """Displays the server info if any."""
    #   serverInfo = self.settings.getServerStat(ctx.guild, "Info")
    #   msg = 'I have no info on *{}* yet.'.format(ctx.guild.name)
    #   if serverInfo:
    #       msg = '*{}*:\n\n{}'.format(ctx.guild.name, serverInfo)
    #   await ctx.send(Utils.suppressed(ctx,msg))

    @commands.command(pass_context=True)
    async def dumpservers(self, ctx):
        """Menyimpan/backup server info dalam format .txt dan di upload private message (owner only)."""
        if not await Utils.is_owner_reply(ctx): return
        timeStamp = datetime.today().strftime("%Y-%m-%d %H.%M")
        serverFile = 'ServerList-{}.txt'.format(timeStamp)
        msg = 'Saving server list to *{}*...'.format(serverFile)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author))
        message = await ctx.author.send(embed = em)
        msg = ''
        for server in self.bot.guilds:
            msg += server.name + "\n"
            msg += str(server.id) + "\n"
            msg += server.owner.name + "#" + str(server.owner.discriminator) + "\n\n"
            msg += str(len(server.members)) + "\n\n"
        # Trim the last 2 newlines
        msg = msg[:-2].encode("utf-8")
        with open(serverFile, "wb") as myfile:
            myfile.write(msg)
        msg = 'Uploading *{}*...'.format(serverFile)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author))
        await message.edit(embed = em)

        await ctx.send(file=discord.File(serverFile))

        msg = 'Uploaded *{}!*'.format(serverFile)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author))
        await message.edit(embed = em)
        os.remove(serverFile)

    @commands.command(pass_context=True)
    async def leaveserver(self, ctx, *, targetServer = None):
        """Pergi dari server yang dituju, membutuhkan nama/id server (owner only)."""
        if not await Utils.is_owner_reply(ctx): return
        if targetServer == None:
            # No server passed
            em = discord.Embed(color = 0XFF8C00, description = "Pergi dari server, membutuhkan nama/id server\n\n"
                                                               "**Panduan**\n"
                                                               "`{}leaveserver [nama/id server]`"
                                                               .format(ctx.prefix))
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\n{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        # Check id first, then name
        guild = next((x for x in self.bot.guilds if str(x.id) == str(targetServer)),None)
        if not guild:
            guild = next((x for x in self.bot.guilds if x.name.lower() == targetServer.lower()),None)
        if guild:
            await guild.leave()
            try:
                msg = "Aku sudah pergi dari server itu."
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author))
                await ctx.send()
            except:
                pass
            return
        msg = "┐(￣ヘ￣;)┌\nAku tidak dapat menemukan server itu."
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author))
        await ctx.send()