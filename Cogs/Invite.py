import asyncio, discord, time
from   discord.ext import commands
from   Cogs import DisplayName, ReadableTime, Nullify

def setup(bot):
    # Add the bot
    settings = bot.get_cog("Settings")
    bot.add_cog(Invite(bot, settings))

class Invite(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.current_requests = []
        self.temp_allowed = []
        self.approval_time = 3600 # 1 hour for an approval to roll off
        self.request_time = 604800 # 7 x 24 x 3600 = 1 week for a request to roll off
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    def _is_submodule(self, parent, child):
        return parent == child or child.startswith(parent + ".")

    async def onserverjoin(self, server):
        # First verify if we're joining servers
        if not self.settings.getGlobalStat("AllowServerJoin",True):
            # Not joining - see if we have temp access to a server
            temp = next((x for x in self.temp_allowed if x[0] == server.id),None)
            if temp:
                self.temp_allowed.remove(temp)
                # Add to our whitelist
                self._whitelist_server(temp[0])
                return False
            try:
                await server.leave()
            except:
                pass
            return True
        return False

    @commands.Cog.listener()
    async def on_guild_remove(self, server):
        # Remove from the whitelist if it exists
        self._unwhitelist_server(server.id)

    async def remove_request(self,user_server):
        # Wait for the allotted time and remove the request if it still exists
        await asyncio.sleep(self.request_time)
        try:
            self.current_requests.remove(user_server)
        except ValueError:
            pass

    async def remove_allow(self,server_id):
        # Wait for the allotted time and remove the temp_allowed value if it still exists
        await asyncio.sleep(self.approval_time)
        try:
            self.temp_allowed.remove(server_id)
        except ValueError:
            pass

    def _check_whitelist(self):
        # Helper method to whitelist all servers based on the "AllowServerJoin" setting - or else just revokes the whitelist entirely
        self.settings.setGlobalStat("ServerWhitelist",None if self.settings.getGlobalStat("AllowServerJoin",True) else [x.id for x in self.bot.guilds])

    def _whitelist_server(self, guild_id = None):
        # Takes a guild id and ensures it's whitelisted
        if not guild_id: return
        current_whitelist = self.settings.getGlobalStat("ServerWhitelist",[])
        current_whitelist = [] if not isinstance(current_whitelist,(list,tuple)) else current_whitelist
        current_whitelist.append(guild_id)
        self.settings.setGlobalStat("ServerWhitelist",current_whitelist)

    def _unwhitelist_server(self, guild_id = None):
        # Takes a guild id and removes it from the whitelist - if it finds it
        if not guild_id: return
        current_whitelist = self.settings.getGlobalStat("ServerWhitelist",[])
        current_whitelist = [] if not isinstance(current_whitelist,(list,tuple)) else [x for x in current_whitelist if not x == guild_id]
        self.settings.setGlobalStat("ServerWhitelist",current_whitelist if len(current_whitelist) else None)

    @commands.Cog.listener()
    async def on_loaded_extension(self, ext):
        # See if we were loaded
        if not self._is_submodule(ext.__name__, self.__module__):
            return
        await self.bot.wait_until_ready()
        # Check if we have the whitelist setup - and if not, auto-whitlelist all joined servers
        if self.settings.getGlobalStat("AllowServerJoin", True): return # No need to check - not restricting
        print("Verifying server whitelist...")
        current_whitelist = self.settings.getGlobalStat("ServerWhitelist",None)
        if not current_whitelist:
            print("No whitelist found - creating one with current servers.")
            return self._check_whitelist() # If we don't have one saved - save one and bail
        # Let's gather a list of any server we're on that's not in the whitelist
        server_list = [x.id for x in self.bot.guilds]
        bail_list = [x for x in server_list if not x in current_whitelist]
        # Leave the unwhitelisted servers
        t = time.time()
        for x in bail_list:
            server = self.bot.get_guild(x)
            print(" - {} not in whitelist - leaving...".format(x))
            try: 
                if server: await server.leave()
            except: print(" --> I couldn't leave {} :(".format(x))
        print("Whitelist verified - took {} seconds.".format(time.time() - t))

    @commands.command()
    async def invite(self, ctx, invite_url = None):
        """Invite bot ini ke server mu."""
        if self.settings.getGlobalStat("AllowServerJoin", True):
            em = discord.Embed(color = 0XFF8C00, description = "> d(=^･ω･^=)b\n"
                                                               "> Yuuk invite aku ke server mu\n"
                                                               "> klik link dibawah ini yaa kak\n"
                                                               "> **[INVITE ME]({})**"
                                                               .format(discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=314561))))
            em.set_author(name = "Invite Link", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        # Check if we're temporarily allowing this server
        server = ctx.guild
        if invite_url:
            try:
                invite = await self.bot.fetch_invite(invite_url)
                server = invite.guild
            except:
                pass
        if server and any(x for x in self.temp_allowed if x[0] == server.id):
            # Got an invite
            em = discord.Embed(color = 0XFF8C00, description = "> d(=^･ω･^=)b\n"
                                                               "> Yuuk invite aku ke server {}\n"
                                                               "> klik link dibawah ini yaa kak\n"
                                                               "> **[INVITE ME]({})**"
                                                               .format(Nullify.clean(server.name),
                                                                       discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=8), guild=server)))
            em.set_author(name = "Invite Link", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        msg = "Kamu membutuhkan persetujuan dari owner ku{} untuk menginvite ke server mu. \nKamu dapat melakukan request dengan cara\n`{}requestjoin [guild_invite_url]`.".format(
              "" if len(self.settings.getOwners()) == 1 else "",
              ctx.prefix
              )
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "Saat mengetik command tanda [] tidak usah digunakan\n{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(embed = em)

    @commands.command()
    async def requestjoin(self, ctx, invite_url = None):
        """Mengirimkan invite url kepada owner bot untuk di review."""
        if self.settings.getGlobalStat("AllowServerJoin", True):
            return await ctx.invoke(self.invite)
        # Get the list of owners - and account for any that have left
        owners = self.settings.getOwners()
        if not len(owners):
            return
        if not invite_url:
            em = discord.Embed(color = 0XFF8C00, description = "Mengirimkan invite url kepada owner bot untuk di review"
                                                               "> **Panduan**\n"
                                                               "> `{}requestjoin discord.gg/invite_url_kamu`")
            em.set_author(name = "Command ignore", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        try:
            invite = await self.bot.fetch_invite(invite_url)
        except:
            msg = "┐(￣ヘ￣;)┌\nInvite link yang kamu berikan tidak valid atau sudah expired."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if invite.guild in self.bot.guilds:
            msg = "( ；￣д￣)\nAku sudah ada di server mu kak."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        temp = next((x for x in self.current_requests if x[1].id == invite.guild.id),None)
        if temp:
            msg = "b(=^‥^=)o\nAku sudah mengirimkan request untuk server mu kak. Request berakhir hingga {}, atau jika sudah disetujui.".format(
                ReadableTime.getReadableTimeBetween(time.time(),temp[2])
            )
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        temp = next((x for x in self.temp_allowed if x[0] == invite.guild.id),None)
        if temp:
            await ctx.invoke(self.invite,invite_url)
            msg = "Berlaku hingga {}.".format(ReadableTime.getReadableTimeBetween(time.time(),temp[1]))
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        # Build a request to dm to up to the first 10 owners
        msg = "{} ({} - {}#{} - {})\ntelah meminta request bot untuk: {} ({})\nmelalui invite link: {}".format(
            DisplayName.name(ctx.author),
            ctx.author.mention,
            Nullify.clean(ctx.author.name),
            ctx.author.discriminator,
            ctx.author.id,
            Nullify.clean(invite.guild.name),
            invite.guild.id,
            invite
        )
        owners = owners if len(owners) < 11 else owners[:10]
        for owner in owners:
            target = self.bot.get_user(int(owner))
            if not target:
                continue
            em = discord.Embed(color = 0XFF8C00, description = msg)
            await target.send(embed = em)
        request = (ctx.author,invite.guild,time.time()+self.request_time,ctx)
        self.current_requests.append(request)
        self.bot.loop.create_task(self.remove_request(request))
        msgDone = "b(=^‥^=)o\nAku telah mengirimkan request mu ke owner ku{} [NvStar]Agy Pascha#9110. Request akan berakhir hingga {}.".format(
            "" if len(owners) == 1 else "",
            ReadableTime.getReadableTimeBetween(0,self.request_time))
        em = discord.Embed(color = 0XFF8C00, description = msgDone)
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)

    @commands.command()
    async def approvejoin(self, ctx, server_id = None):
        """Menyetujui bot sementara untuk bergabung melalui link atau ID server yang telah dikirim (owner-only)."""
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        if server_id == None:
            em = discord.Embed(color = 0XFF8C00, description = "> **Panduan**\n"
                                                               "> {}approvejoin [server_id/invite_url]\n"
                                                               .format(ctx.prefix))
            em.set_author(name = "Command ignore", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        try:
            server_id = int(server_id)
        except:
            try:
                invite = await self.bot.fetch_invite(server_id)
                server_id = invite.guild.id
            except:
                msg = "┐(￣ヘ￣;)┌\nserver ID yang kamu masukan salah."
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                              icon_url = "{}".format(ctx.author.avatar_url))
                return await ctx.send(embed = em)
        guild_list = [x.id for x in self.bot.guilds]
        # Check if we're already on that server, or if it's already been approved
        if server_id in guild_list:
            msg = "( ；￣д￣)\nAku sudah berada di server itu."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        temp = next((x for x in self.temp_allowed if x[0] == server_id),None)
        if temp:
            # Let's remove the approval to allow it to re-add with a new time
            try:
                self.temp_allowed.remove(temp)
            except:
                pass
        # Allow the guild
        temp_allow = (server_id,time.time()+self.approval_time)
        self.temp_allowed.append(temp_allow)
        # Remove if it's been requested
        request = next((x for x in self.current_requests if x[1].id == invite.guild.id),None)
        if request:
            msg = "{}, request mu untuk ku join ke server {} telah disetujui.\nKamu bisa invite aku dengan link dibawah ini:\n**[KLIK DISINI]({})**\n".format(
                request[0].mention,
                Nullify.clean(request[1].name),
                discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=8),guild=request[1])
            )
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "Invite link hanya berlaku untuk {} jam\n{}#{}"
            					 .format(ReadableTime.getReadableTimeBetween(0,self.approval_time),
            					 ctx.author.name,
            					 ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            await request[3].send(embed = em)
            try:
                self.current_requests.remove(request)
            except:
                pass
        self.bot.loop.create_task(self.remove_allow(temp_allow))
        msg = "Aku telah disetujui untuk bergabung dengan server {}\nHingga {}.".format(
            server_id,
            ReadableTime.getReadableTimeBetween(0,self.approval_time))
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)

    @commands.command()
    async def revokejoin(self, ctx, server_id = None):
        """Menolak temporary join yang sudah disetujui (owner-only)."""
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return #await ctx.send('Aku belum ada owner')
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        if server_id == None:
            em = discord.Embed(color = 0XFF8C00, description = "> **Panduan**\n"
                                                               "> {}revokejoin [server_id/invite_url]\n"
                                                               .format(ctx.prefix))
            em.set_author(name = "Command ignore", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        try:
            server_id = int(server_id)
        except:
            try:
                invite = await self.bot.fetch_invite(server_id)
                server_id = invite.guild.id
            except:
                msg = "┐(￣ヘ￣;)┌\nserver ID yang kamu masukan salah.."
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                              icon_url = "{}".format(ctx.author.avatar_url))
                return await ctx.send(embed = em)
        guild_list = [x.id for x in self.bot.guilds]
        # Check if we're already on that server, or if it's already been approved
        if server_id in guild_list:
            msg = "( ；￣д￣)\nAku sudah berada di server itu."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        temp = next((x for x in self.temp_allowed if x[0] == server_id),None)
        if not temp:
            msg = "┐(￣ヘ￣;)┌\nServer tersebut tidak ada dalam temporary approved list."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        self.temp_allowed.remove(temp)
        msg = "Persetujuan untuk bergabung dalam server id {} telah dibatalkan.".format(server_id)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(embed = em)

    @commands.command()
    async def canjoin(self, ctx, *, yes_no = None):
        """Set bot apakah dapat bergabung dengan server baru atau tidak? (owner-only)
        Command default ini selalu *Off*."""
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return #await ctx.send('I have not been claimed, *yet*.')
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        setting_name = "Bot public"
        setting_val  = "AllowServerJoin"
        current = self.settings.getGlobalStat(setting_val, True)
        
        if yes_no == None:
            msg = "{} telah *{}.*".format(setting_name,"dinyalakan\nSemua orang dapat invite bot ini kedalam server mereka masing masing" if current else "dimatikan\nBot hanya bisa invite melalui persetujuan owner")
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
        elif yes_no.lower() in [ "yes", "on", "true", "enabled", "enable" ]:
            yes_no = True
            msg = "{} {} *dinyalakan*.".format(setting_name,"masih" if current else "sekarang")
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
        elif yes_no.lower() in [ "no", "off", "false", "disabled", "disable" ]:
            yes_no = False
            msg = "{} {} *dimatikan*.".format(setting_name,"masih" if not current else "sekarang")
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
        else:
            msg = "That's not a valid setting."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            yes_no = current
        if not yes_no == None and not yes_no == current:
            self.settings.setGlobalStat(setting_val, yes_no)
        # Force the whitelist update
        self._check_whitelist()
        await ctx.send(embed = em)

    @commands.command()
    async def block(self, ctx, *, server : str = None):
        """Block bot ini untuk memasuki server.(owner-only)
        bisa menggunakan nama atau id server maupun nama pemilik server (owner-only).

        Selalu perhatikan huruf Besar/Kecil nama + descriminator pamilik server (Contoh. [ACX] NvStar#9111)."""
        # Check if we're suppressing @here and @everyone mentions
        suppress = True if self.settings.getServerStat(ctx.guild,"SuppressMentions",True) else False
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return #await ctx.send('I have not been claimed, *yet*.')
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        if server == None:
            # No server provided
            em = discord.Embed(color = 0XFF8C00, description = "> **Panduan**\n"
                                                               "> {}block [nama server/id atau nama#desc/id]\n"
                                                               .format(ctx.prefix))
            em.set_author(name = "Command ignore", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        serverList = self.settings.getGlobalStat('BlockedServers',[])
        for serv in serverList:
            if str(serv).lower() == server.lower():
                # Found a match - already blocked.
                msg = "*{}* sudah masuk dalam list blokir!".format(serv)
                if suppress:
                    msg = Nullify.clean(msg)
                return await ctx.send(msg)
        # Not blocked
        serverList.append(server)
        self.settings.setGlobalStat("BlockedServers",serverList)
        msg = "*{}* Telah di blokir!".format(server)
        # Check for suppress
        if suppress:
            msg = Nullify.clean(msg)
        await ctx.send(msg)

    @commands.command()
    async def unblock(self, ctx, *, server : str = None):
        """Membuka blokir server or nama pemilik server (owner-only)."""
        # Check if we're suppressing @here and @everyone mentions
        suppress = True if self.settings.getServerStat(ctx.guild,"SuppressMentions",True) else False
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return #await ctx.send('I have not been claimed, *yet*.')
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        if server == None:
            # No server provided
            em = discord.Embed(color = 0XFF8C00, description = "> **Panduan**\n"
                                                               "> {}unblock [nama server/id atau nama#desc/id]\n"
                                                               .format(ctx.prefix))
            em.set_author(name = "Command ignore", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        serverList = self.settings.getGlobalStat('BlockedServers',[])
        serverTest = [x for x in serverList if not str(x).lower() == server.lower()]
        if len(serverList) != len(serverTest):
            # Something changed
            self.settings.setGlobalStat("BlockedServers",serverTest)
            msg = "*{}* unblocked!".format(server)
            if suppress:
                msg = Nullify.clean(msg)
            return await ctx.send(msg)
        # Not found
        msg = "┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}* dalam daftar blokir ku.".format(server)
        # Check for suppress
        if suppress:
            msg = Nullify.clean(msg)
        await ctx.send(msg)

    @commands.command()
    async def unblockall(self, ctx):
        """Membuka semua server dan pemilik server yang telah diblokir (owner-only)."""
        # Check if we're suppressing @here and @everyone mentions
        suppress = True if self.settings.getServerStat(ctx.guild,"SuppressMentions",True) else False
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return #await ctx.send('I have not been claimed, *yet*.')
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        self.settings.setGlobalStat('BlockedServers',[])
        await ctx.send("*Semua* server dan pemilik server telah di unblock!")

    @commands.command()
    async def blocked(self, ctx):
        """Menampilkan daftar list server dan pemilik server yang di blokir (owner-only)."""
        # Check if we're suppressing @here and @everyone mentions
        suppress = True if self.settings.getServerStat(ctx.guild,"SuppressMentions",True) else False
        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return #await ctx.send('I have not been claimed, *yet*.')
        elif isOwner == False:
            msgText = ["Siapa yaa?\nKamu bukan owner ku",
                       "Kamu bukan owner ku",
                       "Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",
                       "ikjdfahguiyaewgkljasdcbngiuefabhg\nkamu bukan owner ku!!!"]
            msg = random.choice(msgText)
            return await ctx.send(msg)
        serverList = self.settings.getGlobalStat('BlockedServers',[])
        if not len(serverList):
            msg = "┐(￣ヘ￣;)┌\nTidak ada satupun server atau nama pemilik server dalam daftar blokir ku!"
        else:
            msg = "__Currently Blocked:__\n\n{}".format(', '.join(serverList))
        # Check for suppress
        if suppress:
            msg = Nullify.clean(msg)
        await ctx.send(msg)
