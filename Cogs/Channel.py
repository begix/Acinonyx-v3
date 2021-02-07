import asyncio, discord, time, os
from   discord.ext import commands
from   datetime import datetime
from   operator import itemgetter
from   Cogs import Utils, Settings, ReadableTime, DisplayName

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Channel(bot, settings))

# This is the admin module.  It holds the admin-only commands
# Everything here *requires* that you're an admin

class Channel(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    async def member_update(self, before, after):
        # Check if the member went offline and log the time
        if after.status == discord.Status.offline:
            currentTime = int(time.time())
            self.settings.setUserStat(after, after.guild, "LastOnline", currentTime)
        

    @commands.command(pass_context=True)
    async def islocked(self, ctx):
        """Cek jika bot hanya merespon dari admin saja atau tidak?."""
        isLocked = self.settings.getServerStat(ctx.message.guild, "AdminLock")
        await ctx.send("Admin lock *On*.\nSemua member tidak dapat menggunakan bot ini selain **ADMIN**" if isLocked else "Admin lock *Off*.\nSemua member dapat menggunakan bot ini.")
        
        
    @commands.command(pass_context=True)
    async def rules(self, ctx):
        """Menampilkan server rule."""
        rules = self.settings.getServerStat(ctx.guild, "Rules")
        msg = "***{}*** **Rule:**\n{}".format(ctx.guild.name, rules)
        await ctx.send(Utils.suppressed(ctx,msg))


    @commands.command(pass_context=True)
    async def listmuted(self, ctx):
        """Menampilkan list nama member yang di mute."""
        muteList = self.settings.getServerStat(ctx.guild, "MuteList")
        activeMutes = []
        for entry in muteList:
            member = DisplayName.memberForID(entry['ID'], ctx.guild)
            if member:
                # Found one!
                activeMutes.append(DisplayName.name(member))

        if not len(activeMutes):
            await ctx.send("┐(￣ヘ￣;)┌\nTidak ada satupun member yang dalam status mute.")
            return

        # We have at least one member muted
        msg = 'Member saat ini yang di mute:\n\n'
        msg += ', '.join(activeMutes)
        await ctx.send(Utils.suppressed(ctx,msg))
        
        
    @commands.command(pass_context=True)
    async def listadmin(self, ctx):
        """Melihat list admin dan id."""
        promoArray = self.settings.getServerStat(ctx.message.guild, "AdminArray")       
        promoSorted = sorted(promoArray, key=itemgetter('Name'))

        if not len(promoSorted):
            em = discord.Embed(color = 0XFF8C00, description = "> Saat ini tidak ada role admin yang terdaftar.\n> \n"
                                                               "> **Panduan menambahkan admin role**\n"
                                                               "> `{}addadmin [role]`"
                                                               .format(ctx.prefix))
            em.set_author(name = "List Admin", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            roleText = em
            await ctx.send(embed = roleText)
            return
        
        roleText = "__**Current Admin Roles:**__\n\n"

        for arole in promoSorted:
            found = False
            for role in ctx.message.guild.roles:
                if str(role.id) == str(arole["ID"]):
                    # Found the role ID
                    found = True
                    roleText = '{}**{}** (ID : `{}`)\n'.format(roleText, role.name, arole['ID'])
            if not found:
                roleText = '{}**{}** (Dihapus dari server)\n'.format(roleText, arole['Name'])

        await ctx.send(Utils.suppressed(ctx,roleText))


    @commands.command(pass_context=True)
    async def log(self, ctx, messages : int = 25, *, chan : discord.TextChannel = None):
        """Mencatat jumlah pesan dari channel tertentu (admin server-only).
        Log chat akan dicatat sebanyak 25 jika tidak mencamtumkan jumlah message."""
        if not await Utils.is_bot_admin_reply(ctx): return

        timeStamp = datetime.today().strftime("%d-%m-%Y %H.%M")
        logFile = 'Logs-{}.txt'.format(timeStamp)

        if not chan:
            chan = ctx

        # Remove original message
        await ctx.message.delete()

        mess = await ctx.send('Menyimpan log ke *{}*...'.format(logFile))

        # Use logs_from instead of purge
        counter = 0
        msg = ''
        async for message in chan.history(limit=messages):
            counter += 1
            msg += message.content + "\n"
            msg += '----Dikirim-Oleh: ' + message.author.name + '#' + message.author.discriminator + "\n"
            msg += '---------Jam: ' + message.created_at.strftime("%d-%m-%Y %H.%M") + "\n"
            if message.edited_at:
                msg += '--Jam Edited: ' + message.edited_at.strftime("%d-%m-%Y %H.%M") + "\n"
            msg += '\n'

        msg = msg[:-2].encode("utf-8")

        with open(logFile, "wb") as myfile:
            myfile.write(msg)
        
        await mess.edit(content='Uploading *{}*...'.format(logFile))
        await ctx.author.send(file=discord.File(fp=logFile))
        await mess.edit(content='Uploaded *{}!\n*Cek Pesan DM*'.format(logFile))
        os.remove(logFile)
