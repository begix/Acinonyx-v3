import asyncio, discord
from   discord.ext import commands
from   Cogs import Utils, DisplayName, Xp

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Promote(bot, settings))

# This module is for auto promoting/demoting of roles - admin only

class Promote(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    async def _can_run(self, ctx, reply=True):
        # Check if we're admin - and if not, check if bot admins can run this
        # and if we're bot admin
        if Utils.is_admin(ctx): return True
        if self.settings.getServerStat(ctx.guild,"BotAdminAsAdmin",False) and Utils.is_bot_admin_only(ctx): return True
        msg = "┐(￣ヘ￣;)┌\nKamu tidak memiliki hak untuk menggunakan command ini."
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        if reply: await ctx.send(embed = em)
        return False

    @commands.command(pass_context=True)
    async def promote(self, ctx, *, member = None):
        """Menaikan jabatan role xp member ke role xp selanjutnya(admin only)."""
        # Only allow admins to change server stats
        if not await self._can_run(ctx): return
        em = discord.Embed(color = 0XFF8C00, description =  "Menaikan jabatan role xp member ke role xp selanjutnya\n\n"
                                                            "**Panduan**\n"
                                                            "*`{}promote [member]`*"
                                                            .format(ctx.prefix))
        em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan.\n{}".format(ctx.author),
                      icon_url = f"{ctx.author.avatar_url}")

        if member == None:
            return await ctx.send(embed=em)

        memberName = member
        member = DisplayName.memberForName(memberName, ctx.guild)
        if not member:
            msg = Utils.suppressed(ctx, '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName))
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        # Get user's xp
        xp = int(self.settings.getUserStat(member, ctx.guild, "XP"))

        # Get the role list
        promoArray = self.getSortedRoles(ctx.guild)
        currentRole = self.getCurrentRoleIndex(member, ctx.guild)
        nextRole = currentRole + 1
        neededXp = 0
        if nextRole >= len(promoArray):
            msg = '┐(￣ヘ￣;)┌\nTidak ada role yang lebih tinggi untuk promote *{}*.'.format(DisplayName.name(member))
        else:
            newRole  = DisplayName.roleForID(promoArray[nextRole]['ID'], ctx.guild)
            neededXp = int(promoArray[nextRole]['XP'])-xp
            self.settings.incrementStat(member, ctx.guild, "XP", neededXp)
            # Start at the bottom role and add all roles up to newRole
            addRoles = []
            for i in range(0, nextRole+1):
                addRole  = DisplayName.roleForID(promoArray[i]['ID'], ctx.guild)
                if addRole:
                    if not addRole in member.roles:
                        addRoles.append(addRole)
            # await member.add_roles(*addRoles)
            # Use role manager instead
            self.settings.role.add_roles(member, addRoles)
            if not newRole:
                # Promotion role doesn't exist
                msg = '┐(￣ヘ￣;)┌\nSepertinya role **{}** tidak ada dalam server.\n*{}* tetap diberikan sejumlah *{:,} xp*, tapi aku tidak dapat promote ke role yang tidak tercantum dalam list.\nPertimbangkan lagi untuk merevisi role xp.'.format(promoArray[nextRole]['Name'], DisplayName.name(member), neededXp)
            else:
                msg = '*{}* telah memberikan sejumlah *{:,} xp* dan menaikan ke role **{}**!'.format(DisplayName.name(member), neededXp, newRole.name)
            self.bot.dispatch("xp", member, ctx.author, neededXp)
        msgDone = Utils.suppressed(ctx,msg)
        em = discord.Embed(color = 0XFF8C00, description = msgDone)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)

    @commands.command(pass_context=True)
    async def promoteto(self, ctx, *, member = None, role = None):
        """Menaikan jabatan role xp member ke role yang ditentukan(admin only).
        Pastikan role xp sudah terdaftar dalam list."""
        if not await self._can_run(ctx): return
        em = discord.Embed(color = 0XFF8C00, description =  "Menaikan role xp member ke role yang ditentukan\n"
                                                            "Pastikan role xp sudah terdaftar dalam list\n\n"
                                                            "**Panduan**\n"
                                                            "*`{}promoteto [member] [role]`*"
                                                            .format(ctx.prefix))
        em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan.\n{}".format(ctx.author),
                      icon_url = "{}".format(ctx.author.avatar_url))

        if member == None:
            return await ctx.send(embed=em)

        if role == None:
            # Either a role wasn't set - or it's the last section
            if type(member) is str:
                # It' a string - the hope continues
                # Let's search for a name at the beginning - and a role at the end
                parts = member.split()
                memFromName = None
                for j in range(len(parts)):
                    # Reverse search direction
                    i = len(parts)-1-j
                    # Name = 0 up to i joined by space
                    nameStr = ' '.join(parts[0:i+1])
                    # Role = end of name -> end of parts joined by space
                    roleStr = ' '.join(parts[i+1:])
                    memFromName = DisplayName.memberForName(nameStr, ctx.guild)
                    if memFromName:
                        # We got a member - let's check for a role
                        roleFromName = DisplayName.roleForName(roleStr, ctx.guild)
                            
                        if not roleFromName == None:
                            # We got a member and a role - break
                            role = roleFromName
                            break
                if memFromName == None:
                    # Never found a member at all
                    msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}* dalam server.'.format(member)
                    msgDone = Utils.suppressed(ctx,msg)
                    em = discord.Embed(color = 0XFF8C00, description = msgDone)
                    em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                    return await ctx.send(embed = em)
                if roleFromName == None:
                    # We couldn't find one or the other
                    return await ctx.send(embed = em)

                member = memFromName

        # Get user's xp
        xp = int(self.settings.getUserStat(member, ctx.guild, "XP"))

        # Get the role list
        promoArray = self.getSortedRoles(ctx.guild)
        nextRole = self.getIndexForRole(role, ctx.guild)
        currentRole = self.getCurrentRoleIndex(member, ctx.guild)
        vowels = 'aeiou'

        if nextRole == None:
            em = discord.Embed(color = 0XFF8C00, description =  "> ┐(￣ヘ￣;)┌\n"
                                                                "> Role **{}** tidak terdaftar dalam list role xp.\n> \n"
                                                                "> Kamu dapat menambahkan role xp dengan cara:\n"
                                                                "> `{}addxprole [role] [jumlah xp]`"
                                                                .format(role.name,
                                                                        ctx.prefix))
            em.set_author(name = "Role xp tidak terdaftar", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(name = "Saat mengetik command, tanda [] tidak usah digunakan.\nHelp command color", text = f"Request By : {ctx.author.name}", icon_url = f"{ctx.author.avatar_url}")
            return await ctx.send(embed=em)
        
        if currentRole == nextRole:
            # We are already the target role
            if role.name[:1].lower() in vowels:
                msg = '*{}* sudah memiliki role **{}**.'.format(DisplayName.name(member), role.name)
            else:
                msg = '*{}* sudah memiliki role **{}**.'.format(DisplayName.name(member), role.name)
            msgDone = Utils.suppressed(ctx,msg)
            em = discord.Embed(color = 0XFF8C00, description = msgDone)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        elif currentRole > nextRole:
            # We are a higher role than the target
            msg = '*{}* sudah memiliki role **{}** dalam koleksi role mereka.'.format(DisplayName.name(member), role.name)
            msgDone = Utils.suppressed(ctx,msg)
            em = discord.Embed(color = 0XFF8C00, description = msgDone)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        if nextRole >= len(promoArray):
            msg = '┐(￣ヘ￣;)┌\nTidak ada role yang lebih tinggi untuk mempromosikan kenaikan role xp *{}*.'.format(DisplayName.name(member))
        else:
            newRole  = DisplayName.roleForID(promoArray[nextRole]['ID'], ctx.guild)
            neededXp = int(promoArray[nextRole]['XP'])-xp
            self.settings.incrementStat(member, ctx.guild, "XP", neededXp)
            # Start at the bottom role and add all roles up to newRole
            addRoles = []
            for i in range(0, nextRole+1):
                addRole  = DisplayName.roleForID(promoArray[i]['ID'], ctx.guild)
                if addRole:
                    if not addRole in member.roles:
                        addRoles.append(addRole)
            # await member.add_roles(*addRoles)
            # Use role manager instead
            self.settings.role.add_roles(member, addRoles)
            if not newRole:
                # Promotion role doesn't exist
                msg = '┐(￣ヘ￣;)┌\nSepertinya **{}** tidak ada dalam server.\n*{}* akan tetap diberikan sejumlah *{:,} xp*, tapi aku tidak bisa menambahkan role yang tidak ada dalam list. Pertimbangkan lagi untuk merevisi role xp dalam server mu.'.format(promoArray[nextRole]['Name'], DisplayName.name(member), neededXp)
            else:
                msg = '*{}* telah di berikan sejumlah *{:,} xp* dan dinaikan ke role **{}**!'.format(DisplayName.name(member), neededXp, newRole.name)
            self.bot.dispatch("xp", member, ctx.author, neededXp)
        msgDone = Utils.suppressed(ctx,msg)
        em = discord.Embed(color = 0XFF8C00, description = msgDone)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(embed = em)

    @commands.command(pass_context=True)
    async def demote(self, ctx, *, member = None):
        """Menurunkan jabatan role xp kepada member ke role xp dibawahnya(admin only)."""
        if not await self._can_run(ctx): return 
        em = discord.Embed(color = 0XFF8C00, description =  "> Menurunkan jabatan role xp kepada member ke role xp dibawahnya\n> \n"
                                                            "> **Panduan**\n"
                                                            "> `{}demote [member]`"
                                                            .format(ctx.prefix))
        em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan.\n{}".format(ctx.author), icon_url = f"{ctx.author.avatar_url}")

        if member == None:
            return await ctx.send(embed=em)

        if type(member) is str:
            memberName = member
            member = DisplayName.memberForName(memberName, ctx.message.guild)
            if not member:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}* dalam server...'.format(memberName)
                # Check for suppress
                msgDone = Utils.suppressed(ctx,msg)
                em = discord.Embed(color = 0XFF8C00, description = msgDone)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                return await ctx.send(embed = em)

        # Get user's xp
        xp = int(self.settings.getUserStat(member, ctx.guild, "XP"))

        # Get the role list
        promoArray = self.getSortedRoles(ctx.guild)
        currentRole = self.getCurrentRoleIndex(member, ctx.guild)
        nextRole = currentRole - 1
        if nextRole == -1:
            # We're removing the user from all roles
            neededXp = int(promoArray[0]['XP'])-xp-1
            self.settings.incrementStat(member, ctx.guild, "XP", neededXp)
            remRoles = []
            for i in range(0, len(promoArray)):
                remRole  = DisplayName.roleForID(promoArray[i]['ID'], ctx.guild)
                if remRole:
                    if remRole in member.roles:
                        remRoles.append(remRole)
            # await member.remove_roles(*remRoles)
            # Use role manager instead
            self.settings.role.rem_roles(member, remRoles)
            msg = 'sejumlah *{} xp* telah dikurangi dari *{}* dan role dia telah diturunkan dari system xp!'.format(neededXp*-1, DisplayName.name(member))
            self.bot.dispatch("xp", member, ctx.author, neededXp)
        elif nextRole < -1:
            msg = '┐(￣ヘ￣;)┌\nTidak ada role xp yang lebih rendah untuk menurunkan role milik *{}*.'.format(DisplayName.name(member))
        else:
            newRole  = DisplayName.roleForID(promoArray[nextRole]['ID'], ctx.guild)
            neededXp = int(promoArray[nextRole]['XP'])-xp
            self.settings.incrementStat(member, ctx.guild, "XP", neededXp)
            # Start at the currentRole and remove that and all roles above
            remRoles = []
            for i in range(currentRole, len(promoArray)):
                remRole  = DisplayName.roleForID(promoArray[i]['ID'], ctx.guild)
                if remRole:
                    if remRole in member.roles:
                        remRoles.append(remRole)
            # await member.remove_roles(*remRoles)
            # Use role manager instead
            self.settings.role.rem_roles(member, remRoles)
            if not newRole:
                # Promotion role doesn't exist
                msg = '┐(￣ヘ￣;)┌\nSepertinya **{}** sudah tidak ada dalam server. namun sejumlah *{:,} xp* milik *{}* akan tetap dikurangi\n tapi aku tidak dapat menurunkan jabatan role xp, pertimbangkan lagi untuk merevisi role xp dalam server mu.'.format(promoArray[nextRole]['Name'], neededXp*-1, DisplayName.name(member))
            else:
                msg = 'sejumlah *{:,} xp* milik *{}* telah dikurangi dan jabatan role xp telah diturunkan ke **{}**!'.format(neededXp*-1, DisplayName.name(member), newRole.name)
            self.bot.dispatch("xp", member, ctx.author, neededXp)
        msgDone = Utils.suppressed(ctx,msg)
        em = discord.Embed(color = 0XFF8C00, description = msgDone)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(embed = em)

    @commands.command(pass_context=True)
    async def demoteto(self, ctx, *, member = None, role = None):
        """Menurunkan jabatan role xp ke role xp tertentu kepada member(admin only).
        Pastikan role xp sudah terdaftar dalam list"""
        if not await self._can_run(ctx): return
        em = discord.Embed(color = 0XFF8C00, description =  "> Menurunkan jabatan role xp ke role xp tertentu kepada member\n"
                                                            "> Pastikan role xp sudah terdaftar dalam list\n> \n"
                                                            "> **Panduan**\n"
                                                            "> `{}demote [member]`"
                                                            .format(ctx.prefix))
        em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan.\n{}".format(ctx.author), icon_url = f"{ctx.author.avatar_url}")

        if member == None:
            return await ctx.send(embed=em)

        if role == None:
            # Either a role wasn't set - or it's the last section
            if type(member) is str:
                # It' a string - the hope continues
                # Let's search for a name at the beginning - and a role at the end
                parts = member.split()
                memFromName = None
                for j in range(len(parts)):
                    # Reverse search direction
                    i = len(parts)-1-j
                    # Name = 0 up to i joined by space
                    nameStr = ' '.join(parts[0:i+1])
                    # Role = end of name -> end of parts joined by space
                    roleStr = ' '.join(parts[i+1:])
                    memFromName = DisplayName.memberForName(nameStr, ctx.message.guild)
                    if memFromName:
                        # We got a member - let's check for a role
                        roleFromName = DisplayName.roleForName(roleStr, ctx.message.guild)
                            
                        if not roleFromName == None:
                            # We got a member and a role - break
                            role = roleFromName
                            break
                if memFromName == None:
                    # Never found a member at all
                    msg = 'I couldn\'t find *{}* on the server.'.format(member)
                    msgDone = Utils.suppressed(ctx,msg)
                    em = discord.Embed(color = 0XFF8C00, description = msgDone)
                    em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                    return await ctx.send(embed = em)
                if roleFromName == None:
                    # We couldn't find one or the other
                    return await ctx.send(embed = em)

                member = memFromName

        # Get user's xp
        xp = int(self.settings.getUserStat(member, ctx.guild, "XP"))

        # Get the role list
        promoArray = self.getSortedRoles(ctx.guild)
        nextRole = self.getIndexForRole(role, ctx.guild)
        currentRole = self.getCurrentRoleIndex(member, ctx.guild)
        vowels = 'aeiou'
        
        if nextRole == None:
            msg = '┐(￣ヘ￣;)┌\nRole **{}** tidak terdaftar dalam list xp role\nKamu dapat menambahkannya dengan command `{}addxprole [role] [jumlah xp]`.'.format(role.name, ctx.prefix)
            msgDone = Utils.suppressed(ctx,msg)
            em = discord.Embed(color = 0XFF8C00, description = msgDone)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        if currentRole == nextRole:
            # We are already the target role
            if role.name[:1].lower() in vowels:
                msg = '*{}* sudah mendapatkan role **{}**.'.format(DisplayName.name(member), role.name)
            else:
                msg = '*{}* sudah mendapatkan role **{}**.'.format(DisplayName.name(member), role.name)
            msgDone = Utils.suppressed(ctx,msg)
            em = discord.Embed(color = 0XFF8C00, description = msgDone)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        elif currentRole < nextRole:
            # We are a higher role than the target
            msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menurunkan xp role *{}* ke xp role yang lebih tinggi.'.format(DisplayName.name(member))
            msgDone = Utils.suppressed(ctx,msg)
            em = discord.Embed(color = 0XFF8C00, description = msgDone)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(Utils.suppressed(ctx,msg))

        newRole  = DisplayName.roleForID(promoArray[nextRole]['ID'], ctx.guild)
        neededXp = int(promoArray[nextRole]['XP'])-xp
        self.settings.incrementStat(member, ctx.guild, "XP", neededXp)
        # Start at the currentRole and remove that and all roles above
        remRoles = []
        for i in range(currentRole, len(promoArray)):
            remRole  = DisplayName.roleForID(promoArray[i]['ID'], ctx.guild)
            if remRole:
                if remRole in member.roles:
                    # Only add the ones we have
                    remRoles.append(remRole)
        # await member.remove_roles(*remRoles)
        # Use role manager instead
        self.settings.role.rem_roles(member, remRoles)
        if not newRole:
            # Promotion role doesn't exist
            msg = '┐(￣ヘ￣;)┌\nSepertinya **{}** sudah tidak ada dalam server. namun sejumlah *{:,} xp* milik *{}* akan tetap dikurangi\n tapi aku tidak dapat menurunkan jabatan role xp, pertimbangkan lagi untuk merevisi role xp dalam server mu.'.format(promoArray[nextRole]['Name'], neededXp*-1, DisplayName.name(member))
        else:
            msg = 'sejumlah *{:,} xp* milik *{}* telah dikurangi dan jabatan role xp telah diturunkan ke **{}**!'.format(neededXp*-1, DisplayName.name(member), newRole.name)
        self.bot.dispatch("xp", member, ctx.author, neededXp)
        msgDone = Utils.suppressed(ctx,msg)
        em = discord.Embed(color = 0XFF8C00, description = msgDone)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(embed = em)

    def getCurrentRoleIndex(self, member, server):
        # Helper method to get the role index the user *should* have
        # Get user's xp
        xp = int(self.settings.getUserStat(member, server, "XP"))
        promoSorted = self.getSortedRoles(server)
        index = 0
        topIndex = -1
        for role in promoSorted:
            if int(role['XP']) <= xp:
                topIndex = index
            index += 1
        return topIndex

    def getIndexForRole(self, role, server):
        # Helper method to get the sorted index for an xp role
        # Returns None if not found
        promoSorted = self.getSortedRoles(server)
        index = 0
        found = False
        for arole in promoSorted:
            if str(arole['ID']) == str(role.id):
                # Found it - break
                found = True
                break
            index += 1
        if found:
            return index
        return None

    def getSortedRoles(self, server):
        # Get the role list
        promoArray = self.settings.getServerStat(server, "PromotionArray")
        if not type(promoArray) is list:
            promoArray = []
        # promoSorted = sorted(promoArray, key=itemgetter('XP', 'Name'))
        promoSorted = sorted(promoArray, key=lambda x:int(x['XP']))
        return promoSorted
