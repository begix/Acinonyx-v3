import asyncio, discord, random
from   discord.ext import commands
from   Cogs import Utils, Xp, DisplayName, CheckRoles

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Feed(bot, settings))

# This is the feed module.  It allows the bot to be fed,
# get hungry, die, be resurrected, etc.

class Feed(commands.Cog):

    # Init with the bot reference, and a reference to the settings var and xp var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.loop_list = []
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    # Proof of concept stuff for reloading cog/extension
    def _is_submodule(self, parent, child):
        return parent == child or child.startswith(parent + ".")

    def _can_xp(self, user, server):
        # Checks whether or not said user has access to the xp system
        requiredXP  = self.settings.getServerStat(server, "RequiredXPRole")
        promoArray  = self.settings.getServerStat(server, "PromotionArray")
        userXP      = self.settings.getUserStat(user, server, "XP")
        if not requiredXP:
            return True

        for checkRole in user.roles:
            if str(checkRole.id) == str(requiredXP):
                return True
        # Still check if we have enough xp
        for role in promoArray:
            if str(role["ID"]) == str(requiredXP):
                if userXP >= role["XP"]:
                    return True
                break
        return False

    @commands.Cog.listener()
    async def on_unloaded_extension(self, ext):
        # Called to shut things down
        if not self._is_submodule(ext.__name__, self.__module__):
            return
        for task in self.loop_list:
            task.cancel()

    @commands.Cog.listener()
    async def on_loaded_extension(self, ext):
        # See if we were loaded
        if not self._is_submodule(ext.__name__, self.__module__):
            return
        self.loop_list.append(self.bot.loop.create_task(self.getHungry()))
        
    async def message(self, message):
        # Check the message and see if we should allow it.
        current_ignore = self.settings.getServerStat(message.guild, "IgnoreDeath")
        if current_ignore:
            return { 'Ignore' : False, 'Delete' : False }
        ignore = delete = False
        hunger = int(self.settings.getServerStat(message.guild, "Hunger"))
        hungerLock = self.settings.getServerStat(message.guild, "HungerLock")
        isKill = self.settings.getServerStat(message.guild, "Killed")
        # Get any commands in the message
        context = await self.bot.get_context(message)
        if (isKill or hunger >= 100 and hungerLock):
            ignore = not context.command or not context.command.name in [ "iskill", "resurrect", "hunger", "feed" ]
        # Check if admin and override
        if Utils.is_bot_admin(context):
            ignore = delete = False 
        return { 'Ignore' : ignore, 'Delete' : delete}

    async def getHungry(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            # Add The Hunger
            await asyncio.sleep(900) # runs every 15 minutes
            for server in self.bot.guilds:
                # Iterate through the servers and add them
                isKill = self.settings.getServerStat(server, "Killed")
                if not isKill:
                    hunger = int(self.settings.getServerStat(server, "Hunger"))
                    # Check if hunger is 100% and increase by 1 if not
                    hunger += 1
                    hunger = 100 if hunger > 100 else hunger
                    self.settings.setServerStat(server, "Hunger", hunger)

    @commands.command(pass_context=True)
    async def ignoredeath(self, ctx, *, yes_no = None):
        """Mengabaikan kematian bot saat bot kelaparan didalam server (admin only, settingan default ini selalu off)."""
        if not await Utils.is_bot_admin_reply(ctx): return
        await ctx.send(Utils.yes_no_setting(ctx,"Ignore death","IgnoreDeath",yes_no))

    @commands.command(pass_context=True)
    async def hunger(self, ctx):
        """Tingkat kelaparan bot."""
        hunger = int(self.settings.getServerStat(ctx.guild, "Hunger"))
        isKill = self.settings.getServerStat(ctx.guild, "Killed")
        overweight = hunger * -1
        if hunger <= -1:
            msg = '(;*´Д`)ﾉ\nAku sudah kenyang ({:,}%)... Aku harus berhenti makan untuk sejenak...'.format(overweight)
            foot = ' '
        elif hunger <= -10:
            msg = '（；￣д￣)\nAku gemuk ({:,}%)... Aku akan bertambah semakin gemuk jika kamu terus memberiku makan.'.format(overweight)
            foot = ' '
        elif hunger <= -25:
            msg = '(一。一;; )\nAku sangat gemuk sekarang ({:,}%)... oke waktunya diet?'.format(overweight)
            foot = ' '
        elif hunger <= -50:
            msg = '（ー△ー； )\nAku obesitas sekarang ({:,}%)... Makanan adalah musuh ku sekarang.'.format(overweight)
            foot = ' '
        elif hunger <= -75:
            msg = '(ﾉ￣д￣)ﾉ\nLihat aku sekarang sudah gemuk banget ({:,}%)... Apakah kalian tidak memikirkan kesahatan *ku*?'.format(overweight)
            foot = ' '
        elif hunger <= -100:
            msg = '(✖╭╮✖)\nAku akan mati jika kamu terus memberiku makan ({:,}%). Ku harap kalian bahagia.'.format(overweight)
            foot = ' '
        elif hunger <= -150:
            msg = '(✖﹏✖)\nAku telah mati karena terlalu banyak makan ({:,}%).  Kamu membutuhkan `{}resurrect` untuk menghidupkan ku kembali.'.format(overweight, ctx.prefix)
            foot = ' '
        elif hunger == 0:
            msg = 'o(≧∇≦o)\nAku sudah kenyang ({:,}%). Kalian sekarang aman.\n*untuk saat ini.*'.format(overweight)
            foot = 'ketik \"{}feed [jumlah xp]\" untuk memberi makan bot'.format(ctx.prefix)
        elif hunger <= 15:
            msg = '(￣▽￣)ノ\nAku sudah hampir kenyang ({:,}%). Aku senang sekali!'.format(overweight)
            foot = 'ketik \"{}feed [jumlah xp]\" untuk memberi makan bot'.format(ctx.prefix)
        elif hunger <= 25:
            msg = ' ( ՞ ڡ ՞ )\nAku sedikit lapar ({:,}%). mungkin dari kalian ada yang ingin memberi ku makan?'.format(overweight)
            foot = 'ketik \"{}feed [jumlah xp]\" untuk memberi makan bot'.format(ctx.prefix)
        elif hunger <= 50:
            msg = '༼ ˘ ۝ ˘ ༽\n Aku lapar sekarang({:,}%). Tolong beri aku makan.'.format(overweight)
            foot = 'ketik \"{}feed [jumlah xp]\" untuk memberi makan bot'.format(ctx.prefix)
        elif hunger <= 75:
            msg = '｡ﾟ(*´□`)ﾟ｡\n Aku Kepalaran **sekarang** ({:,}%)!  Apakah kamu menginginkan ku *mati*?'.format(overweight)
            foot = 'ketik \"{}feed [jumlah xp]\" untuk memberi makan bot'.format(ctx.prefix)
        else:
            msg = '=͟͟͞͞( •̀д•́)))\nAku **SANGAT LAPARR!!** ({:,}%)! Beri aku makan atau aku akan *mati*!*'.format(overweight)
            foot = 'ketik \"{}feed [jumlah xp]\" untuk memberi makan bot'.format(ctx.prefix)
        if isKill and hunger > -150:
            msg = '❌ Aku telah *Mati*. Karena kurang perawatan.\nHubungi admin server untuk menggunakan `{}resurrect` Agar aku hidup kembali.'.format(ctx.prefix)
            foot = ' '
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        em.set_footer(text = foot)
        await ctx.send(embed = em)
        
    @commands.command(pass_context=True)
    async def feed(self, ctx, food : int = None):
        """Memberi makan bot dengan XP yang kalian miliki!"""
        # feed the bot, and maybe you'll get something in return!
        msg = '`{}feed [Jumlah XP]`'.format(ctx.prefix)
        em = discord.Embed(color = 0XFF8C00, description = "> Memberi makan bot dengan XP yang kalian miliki!"
                                                           "> **Panduan**"
                                                           "> {}"
                                                           .format(msg))
        if food == None:
            return await channel.send(embed = em)
            
        if not type(food) == int:
            return await channel.send(embed = em)

        isAdmin    = Utils.is_admin(ctx)
        isBotAdmin = Utils.is_bot_admin_only(ctx)
        botAdminAsAdmin = self.settings.getServerStat(ctx.guild, "BotAdminAsAdmin")
        adminUnlim = self.settings.getServerStat(ctx.guild, "AdminUnlimited")
        reserveXP  = self.settings.getUserStat(ctx.author, ctx.guild, "XPReserve")
        minRole    = self.settings.getServerStat(ctx.guild, "MinimumXPRole")
        requiredXP = self.settings.getServerStat(ctx.guild, "RequiredXPRole")
        isKill     = self.settings.getServerStat(ctx.guild, "Killed")
        hunger     = int(self.settings.getServerStat(ctx.guild, "Hunger"))
        xpblock    = self.settings.getServerStat(ctx.guild, "XpBlockArray")

        approve = True
        decrement = True

        # Check Food

        if food > int(reserveXP):
            approve = False
            msg = '┐(￣ヘ￣;)┌\nKamu tidak dapat memberi ku makan dengan xp *{:,}*\nKamu hanya memiliki *{:,}* xp tersimpan!'.format(food, reserveXP)
            
        if food < 0:
            msg = '(҂⌣̀_⌣́) kamu tidak bisa memberiku makan dengan xp kurang dari 0.\nKamu pikir itu lucu?!'
            approve = False
            # Avoid admins gaining xp
            decrement = False
            
        if food == 0:
            msg = '┐(￣ヘ￣;)┌\nKamu tidak dapat memberi ku makan dengan xp *0*'
            approve = False

        # RequiredXPRole
        if not self._can_xp(ctx.author, ctx.guild):
            approve = False
            msg = '┐(￣ヘ￣;)┌\nKamu tidak memiliki permission untuk memberiku makan.'

        # Check bot admin
        if isBotAdmin and botAdminAsAdmin:
            # Approve as admin
            approve = True
            if adminUnlim:
                # No limit
                decrement = False
            else:
                if food < 0:
                    # Don't decrement if negative
                    decrement = False
                if food > int(reserveXP):
                    # Don't approve if we don't have enough
                    msg = '┐(￣ヘ￣;)┌\nKamu tidak dapat memberi ku makan dengan xp *{:,}*\nKamu hanya memiliki *{:,}* xp tersimpan!'.format(food, reserveXP)
                    approve = False
            
        # Check admin last - so it overrides anything else
        if isAdmin:
            # No limit - approve
            approve = True
            if adminUnlim:
                # No limit
                decrement = False
            else:
                if food < 0:
                    # Don't decrement if negative
                    decrement = False
                if food > int(reserveXP):
                    # Don't approve if we don't have enough
                    msg = '┐(￣ヘ￣;)┌\nKamu tidak dapat memberi ku makan dengan *{:,} xp*\nKamu hanya memiliki *{:,}* xp tersimpan!'.format(food, reserveXP)
                    approve = False
            
        # Check if we're blocked
        if ctx.author.id in xpblock:
            msg = "┐(￣ヘ￣;)┌\nKamu tidak dapat memberi makan bot!"
            approve = False
        else:
            if any(x for x in ctx.author.roles if x.id in xpblock):
                msg = "┐(￣ヘ￣;)┌\nRole kamu tidak dapat memberi makan bot!"
                approve = False

        if approve:
            # Feed was approved - let's take the XPReserve right away
            # Apply food - then check health
            hunger -= food
            
            self.settings.setServerStat(ctx.guild, "Hunger", hunger)
            takeReserve = -1*food
            if decrement:
                self.settings.incrementStat(ctx.author, ctx.guild, "XPReserve", takeReserve)

            if isKill:
                # Bot's dead...
                msg = '*{}* Secara perlahan memberikan *{:,} xp* kepada *{}* yang telah mati...\nApakah mungkin akan bangkit suatu saat nanti?'.format(DisplayName.name(ctx.author), food, DisplayName.serverNick(self.bot.user, ctx.guild))
                em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
                return await ctx.send(embed = em)
            
            # Bet more, less chance of winning, but more winnings!
            chanceToWin = 50
            payout = int(food*2)
            
            # 1/chanceToWin that user will win - and payout is double the food
            randnum = random.randint(1, chanceToWin)
            if randnum == 1:
                # YOU WON!!
                self.settings.incrementStat(ctx.author, ctx.guild, "XP", int(payout))
                msg = '*{}* Secara perlahan memberikan *{:,} xp* kepada *{}* yang telah mati...\nApakah mungkin akan bangkit suatu saat nanti?*'.format(DisplayName.name(ctx.author), food, int(payout))
                
                # Got XP - let's see if we need to promote
                await CheckRoles.checkroles(ctx.author, ctx.channel, self.settings, self.bot)
            else:
                msg = '*{}* Memberi ku makan dengan *{:,} xp!*\nTerima kasih banyak!!'.format(ctx.author, food)
        
            if hunger <= -150:
                # Kill the bot here
                self.settings.setServerStat(ctx.guild, "Killed", True)
                self.settings.setServerStat(ctx.guild, "KilledBy", ctx.author.id)
                msg = '{}\n\nAku dibunuh...\n\n*{}* pelakunya...'.format(msg, DisplayName.name(ctx.author.id))          
            elif hunger <= -100:
                msg = '{}\n\nApakah kamu mencoba membunuh ku?\nBerhentilah jika kamu memiliki hati!'.format(msg)
            elif hunger <= -75:
                msg = '{}\n\n（；￣д￣)\nAku sudah terlalu gemuk sekarangdan kesehatan ku menurun.\n Apa kamu memikirkan kesehatan ku??'.format(msg)
            elif hunger <= -50:
                msg = '{}\n\n（；￣д￣) Aku obesitas.\nMakanan adalah musuh ku sekarang.'.format(msg)
            elif hunger <= -25:
                msg = '{}\n\n（；￣д￣)\nAku gemuk.\noke waktunya diet?'.format(msg)  
            elif hunger <= -10:
                msg = '{}\n\n（；￣д￣)\nAku gemuk.\nAku akan bertambah semakin gemuk jika kamu terus memberiku makan.'.format(msg)
            elif hunger <= -1:
                msg = '{}\n\n(;*´Д`)ﾉ\nAku sudah kenyang.\nAku harus berhenti makan untuk sejenak...'.format(msg)
            elif hunger == 0:
                msg = '{}\n\n(;*´Д`)ﾉ\nJika kamu terus memberiku makan, aku akan menjadi gemuk...'.format(msg)
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)
        
    @commands.command(pass_context=True)
    async def kill(self, ctx):
        """Bunuh botnya(Admin-server only)
        Dasar manusia tidak punya perasaan!"""
        # Check for role requirements
        requiredRole = self.settings.getServerStat(ctx.guild, "RequiredKillRole")
        
        # isOwner = self.settings.isOwner(ctx.author)
        # if isOwner == False:
        #     msgText = ["Hus hus..\nFitur ini sedang dalam tahap pengambangan"]
        #     msg = random.choice(msgText)
        #     return await ctx.send(msg)
        
        if requiredRole == "":
            #admin only
            if not await Utils.is_admin_reply(ctx): return
        else:
            #role requirement
            if not any(x for x in ctx.author.roles if str(x.id) == str(requiredRole)) and not Utils.is_admin(ctx):
                em = discord.Embed(color = 0XFF8C00,
                                   description = "> ┐(￣ヘ￣;)┌\n> Kamu tidak memiliki izin untuk menggunakan command ini")
                em.set_author(name = "⚠ ADMIN ONLY", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
                em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
                return await ctx.send(embed=em)

        iskill = self.settings.getServerStat(ctx.guild, "Killed")
        if iskill:
            killedby = self.settings.getServerStat(ctx.guild, "KilledBy")
            killedby = DisplayName.memberForID(killedby, ctx.guild)
            msg = 'Aku telah dibunuh...\n*{}* Pelakunya...'.format(DisplayName.name(killedby))
            em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
        self.settings.setServerStat(ctx.guild, "Killed", True)
        self.settings.setServerStat(ctx.guild, "KilledBy", author.id)
        msg = 'Aku telah dibunuh...\n*{}* Pelakunya...'.format(DisplayName.name(ctx.author.mention))
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)
        
    @commands.command(pass_context=True)
    async def resurrect(self, ctx):
        """Menghidupkan bot yang telah mati.(Admin-server only)"""
        # Check for role requirements
        requiredRole = self.settings.getServerStat(ctx.guild, "RequiredKillRole")
        # isOwner = self.settings.isOwner(ctx.author)
        # if isOwner == False:
        #     msgText = ["Hus hus..\nFitur ini sedang dalam tahap pengambangan"]
        #     msg = random.choice(msgText)
        #     return await ctx.send(msg)
        if requiredRole == "":
            #admin only
            if not await Utils.is_admin_reply(ctx): return
        else:
            #role requirement
            if not any(x for x in ctx.author.roles if str(x.id) == str(requiredRole)) and not Utils.is_admin(ctx):
                msg = "┐(￣ヘ￣;)┌\nKamu tidak memiliki izin untuk menggunakan command ini."
                em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
                return await ctx.send(embed = em)

        iskill = self.settings.getServerStat(ctx.guild, "Killed")
        if not iskill:
            em = discord.Embed(color = 0XFF8C00,
                               description = "┐(￣ヘ￣;)┌\nAku masih hidup.\nuntuk apa kamu menggunakan command ini?")
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
        self.settings.setServerStat(ctx.guild, "Killed", False)
        self.settings.setServerStat(ctx.guild, "Hunger", "0")
        killedby = self.settings.getServerStat(ctx.guild, "KilledBy")
        killedby = DisplayName.memberForID(killedby, ctx.guild)
        msg = 'Tebak siapa yang kembali??\nMungkin *{}* akan membunuhku lagi!*'.format(DisplayName.name(killedby))
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)
        
    @commands.command(pass_context=True)
    async def iskill(self, ctx):
        """Cek apakah bot telah mati?."""
        isKill = self.settings.getServerStat(ctx.guild, "Killed")
        killedBy = self.settings.getServerStat(ctx.guild, "KilledBy")
        killedBy = DisplayName.memberForID(killedBy, ctx.guild)
        msg = 'Aku tidak tau apa yang kamu bicarakan...\nHaruskah aku khawatir soal itu?'
        if isKill:
            msg = 'Aku telah dibunuh...\n*{}* Pelakunya...'.format(DisplayName.name(killedBy))
        else:
            msg = 'Tunggu...\nApakah kamu bertanya aku telah *mati*?'
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)

    @commands.command(pass_context=True)
    async def setkillrole(self, ctx, *, role : discord.Role = None):
        """Set role yang dibutuhkan untuk melakukan kill/resurrect bot (admin-server only)."""
        if not await Utils.is_admin_reply(ctx): return
        if role == None:
            self.settings.setServerStat(ctx.guild, "RequiredKillRole", "")
            msg = '> Kill/resurrect bot hanya dapat dilakukan oleh *admin-server*.'
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "⚠ ADMIN ONLY", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        if type(role) is str:
            try:
                role = discord.utils.get(ctx.server.roles, name=role)
            except:
                msg = "Role yang kamu pilih tidak ditemukan!"
                em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
                await ctx.send(embed = em)
                return
        # If we made it this far - then we can add it
        self.settings.setServerStat(ctx.guild, "RequiredKillRole", role.id)

        msg = 'Role kill/resurrect telah di set ke <@&{}>.'.format(role.id)
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        await ctx.send(embed = em)
        #await ctx.send(Utils.suppressed(ctx,msg))

    @setkillrole.error
    async def killrole_error(self, ctx, error):
        # do stuff
        msg = 'setkillrole Error: {}'.format(error)
        await ctx.send(msg)

    @commands.command(pass_context=True)
    async def killrole(self, ctx):
        """Melihat list role yang dibutuhkan untuk menggunakan command kill/resurrect untuk bot."""
        role = self.settings.getServerStat(ctx.guild, "RequiredKillRole")
        if role == None or role == "":
            msg = 'Hanya **Admin-server** yang dapat menggunakan command kill/ressurect.'
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "⚠ ADMIN ONLY", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(msg)
        # Role is set - let's get its name
        arole = next((x for x in ctx.guild.roles if str(x.id) == str(role)),None)
        if not arole:
            msg = 'Tidak ada role yang cocok dengan ID: `{}`.'.format(role)
        # msg = 'Kamu membutuhkan role **{}** untuk menggunakan command kill/ressurect.'.format(arole.name)
        msg = 'Kamu membutuhkan role <@&{}> untuk menggunakan command kill/ressurect.'.format(role)
        em = discord.Embed(color = 0XFF8C00, description = "{}".format(msg))
        await ctx.send(embed = em)
        # await ctx.send(Utils.suppressed(ctx,msg))
