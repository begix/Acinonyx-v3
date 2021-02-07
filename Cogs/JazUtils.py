import asyncio
import discord
import random
import datetime
import colorsys
from   discord.ext import commands
from   Cogs import DisplayName
from   Cogs import Nullify


# constant for paginating embeds
EMBED_MAX_LEN = 2048
MAX_USERS = 30 # max people to list for !whohas
STATUSMAP1 = {discord.Status.online:'1',discord.Status.dnd:'2',discord.Status.idle:'3'} ##for sorting
STATUSMAP2 = {discord.Status.online:'<:online:768401856731807784>',discord.Status.dnd:'<:dnd:768402324405092362>',discord.Status.idle:'<:idle:768402412045729802>',discord.Status.offline:'<:offline:768402297406357524>'}


def setup(bot):
    # Add the bot
    bot.add_cog(JazUtils(bot))

class JazUtils(commands.Cog):
    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(pass_context=True)
    # async def snowflake(self, ctx, *, sid : str = None):
    #     """show the date a snowflake ID was created"""

    #     sid = int(sid)
    #     timestamp = ((sid >> 22) + 1420070400000) / 1000 # python uses seconds not milliseconds
    #     cdate = datetime.datetime.utcfromtimestamp(timestamp)
    #     msg = "Snowflake created {}".format(cdate.strftime('%A, %B %d %Y at %H:%M:%S UTC'))
    #     return await ctx.send(msg)

    # @commands.command(pass_context=True)
    # async def fullsnowflake(self, ctx, *, sid : str = None):
    #     """show all available data about a snowflake ID"""
    #     sid = int(sid)
    #     timestamp = ((sid >> 22) + 1420070400000) / 1000 # python uses seconds not milliseconds
    #     iwid = (sid & 0x3E0000) >> 17
    #     ipid = (sid & 0x1F000) >> 12
    #     icount = sid & 0xFFF

    #     cdate = datetime.datetime.utcfromtimestamp(timestamp)
    #     fdate = cdate.strftime('%A, %B %d %Y at %H:%M:%S UTC')

    #     embed = discord.Embed(title=sid, description='Discord snowflake ID')
    #     embed.add_field(name="Date created", value=fdate)
    #     embed.add_field(name="Internal worker/process", value="{}/{}".format(iwid,ipid))
    #     embed.add_field(name="Internal counter", value=icount)
    #     embed.add_field(name="As user ping", value="<@{}>".format(sid))
    #     embed.add_field(name="As channel ping", value="<#{}>".format(sid))
    #     embed.add_field(name="As role ping", value="<@&{}>".format(sid))
    #     embed.add_field(name="As custom emote", value="<:test:{}>".format(sid))
    #     embed.add_field(name="As animated emote", value="<a:test:{}>".format(sid))

    #     await ctx.send(embed=embed)


    ## role listing and queries

    def role_check(self, user, role_query):
        # returns True or False if a user has named role
        return any((role.name in role_query for role in user.roles))

    def alphanum_filter(self, text):
        # filter for searching a role by name without having to worry about case or punctuation
        return ''.join(i for i in text if i.isalnum()).lower()

    def rolelist_filter(self, roles, id_list):
        # filters the full role hierarchy based on the predefined lists above
        return [role for role in roles if int(role.id) in id_list]

    def get_named_role(self, server, rolename):
        # finds a role in a server by name
        check_name = self.alphanum_filter(rolename)
        return next((role for role in server.roles if self.alphanum_filter(role.name) == check_name),None)

    def role_accumulate(self, check_roles, members):
        ## iterate over the members to accumulate a count of each role
        rolecounts = {}
        for role in check_roles: # populate the accumulator dict
            if not role.is_default():
                rolecounts[role] = 0

        for member in members:
            for role in member.roles:
                if role in check_roles and not role.is_default(): # want to exclude @everyone from this list
                    rolecounts[role] += 1

        return rolecounts

    async def rolelist_paginate(self, ctx, rlist, title='Role List'):
        # takes a list of roles and counts and sends it out as multiple embed as nessecary
        pages = []
        buildstr = ''
        for role,count in rlist: # this generates and paginates the info
            line = '{:,} {}\n'.format(count,role.mention)
            if len(buildstr) + len(line) > EMBED_MAX_LEN:
                pages.append(buildstr) # split the page here
                buildstr = line
            else:
                buildstr += line
        if buildstr:
            pages.append(buildstr) #if the string has data not already listed in the pages, add it

        for index,page in enumerate(pages): # enumerate so we can add a page number
            embed = discord.Embed(color = 0XFF8C00,title='{} halaman {:,}/{:,}'.format(title, index+1, len(pages)), description=page)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def roles(self, ctx, sort_order:str='name'):
        """Menampilkan role and jumlah member yang mempunyai role tersebut.
        Membutuhkan 1 argument 
        (optional, jika tidak memasukan argument akan mengurutkan role sesuai default)
        mengurutkan role sesuai: default, name, count, atau rainbow"""

        sort_order = sort_order.lower()
        confirm = ['ya']
        msgConfirm = "Command ini mungkin akan membuat list embed yang panjang.\nKetik `ya` untuk melanjutkan"
        em = discord.Embed(color = 0XFF8C00, description = msgConfirm)
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        Msg = await ctx.send(embed = em)
        try:
            msg = await self.bot.wait_for('message', timeout=15, check=lambda msg: msg.author == ctx.author)
        except:
            await Msg.delete()
            msgConfirm = 'Waktu habis, command mu telah dibatalkan'
            em = discord.Embed(color = 0XFF8C00, description = msgConfirm)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em, delete_after=10)
        message = str(msg.content.lower())

        if message not in confirm and message not in ['ya']:
            await Msg.delete()
            msgConfirm = 'Command dibatalkan.\nKamu memasukan konfirmasi yang salah'
            em = discord.Embed(color = 0XFF8C00, description = msgConfirm)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em, delete_after=10)

        if not sort_order in ['default', 'name', 'count', 'rainbow']: # make sure it has valid args
            msgOrder = "Argument yang kamu masukan salah.\nKetik `{}help roles` untuk bantuan.".format(ctx.prefix)
            em = discord.Embed(color = 0XFF8C00, description = msgOrder)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
        await Msg.delete()
        check_roles = ctx.guild.roles # we use roles for these because sometimes we want to see the order
        
        ## now we iterate over the members to accumulate a count of each role
        rolecounts = self.role_accumulate(check_roles, ctx.guild.members)
        
        sorted_list = []
        if sort_order == 'default': # default sort = the server role hierarchy
            for role in check_roles:
                if role in rolecounts:
                    sorted_list.append((role, rolecounts.get(role,0)))
        elif sort_order == 'name': # name sort = alphabetical by role name
            sorted_list = sorted(rolecounts.items(), key=lambda tup: tup[0].name.lower())
        elif sort_order == 'count': # count sort = decreasing member count
            sorted_list = sorted(rolecounts.items(), key=lambda tup: tup[1], reverse=True)
        elif sort_order == 'rainbow': # color sort: by increasing hue value in HSV color space
            sorted_list = sorted(rolecounts.items(), key=lambda tup: colorsys.rgb_to_hsv(tup[0].color.r, tup[0].color.g, tup[0].color.b)[0])
        
        if not sorted_list: # another failsafe
            return

        await self.rolelist_paginate(ctx,sorted_list) # send the list to get actually printed to discord

    @commands.command(pass_context=True)
    async def rolecall(self, ctx, *, rolename):
        """Menghitung jumlah member berdasarkan nama role.
        NB: nama role kalo bisa di ketik biasa yaa tapi jangan di mention, biar nggk ganggu member yang lain"""
        check_role = self.get_named_role(ctx.guild, rolename)
        if not check_role:
            msg = "┐(￣ヘ￣;)┌\nAku tidak dapat menemukan role itu!"
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        count = 0
        online = 0
        for member in ctx.guild.members:
            if check_role in member.roles:
                count += 1
                if member.status != discord.Status.offline:
                    online += 1

        embed = discord.Embed(title=check_role.name, description='{:,}/{:,} online ({:,g}%)'.format(online, count, round((online/count)*100, 2)), color=0XFF8C00)
        embed.set_footer(text='ID: {}\n{}#{}'.format(check_role.id, ctx.author.name, ctx.author.discriminator),
                         icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def whohas(self, ctx, *, rolename):
        """Menampikan list member dengan spesifik nama role.
        NB: nama role kalo bisa di ketik yaa tapi jangan di mention, biar nggk ganggu member yang lain

        diurutkan berdasarkan Online -> Idle -> DnD -> Offline.
        
        Options tersedia(optional):
        -nick
        -username
        
        Contoh:
        acx whohas nama_role
        acx whohas nama_role -nick"""
        mode = 0 # tells how to display: 0 = just mention, 1 = add nickname, 2 = add username
        rolename = rolename.lower()
        if '-nick' in rolename:
            mode = 1
            rolename = rolename.replace('-nick','')
        elif '-username' in rolename:
            mode = 2
            rolename = rolename.replace('-username','')

        check_role = self.get_named_role(ctx.guild, rolename)
        if not check_role:
            msg = "┐(￣ヘ￣;)┌\nAku tidak dapat menemukan role itu!"
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        users = [member for member in ctx.guild.members if check_role in member.roles]

        sorted_list = sorted(users, key=lambda usr: (STATUSMAP1.get(usr.status,'4')) + (usr.nick.lower() if usr.nick else usr.name.lower()))
        truncated = False
        if len(sorted_list) > MAX_USERS:
            sorted_list = sorted_list[:MAX_USERS] ## truncate to the limit
            truncated = True
        if mode == 2: # add full username
            page = '\n'.join('{} {} ({}#{})'.format(STATUSMAP2.get(member.status, '<:offline:768402297406357524>'), member.mention, member.name, member.discriminator) for member in sorted_list) # not bothering with multiple pages cause 30 members is way shorter than one embed
        elif mode == 1: # add nickname
            page = '\n'.join('{} {} ({})'.format(STATUSMAP2.get(member.status, '<:offline:768402297406357524>'), member.mention, member.display_name) for member in sorted_list)
        else:
            page = '\n'.join('{} {}'.format(STATUSMAP2.get(member.status, '<:offline:768402297406357524>'), member.mention) for member in sorted_list)

        if truncated:
            page += '\n*dan masih ada {} member lainnya...*'.format(len(users) - MAX_USERS)

        embed = discord.Embed(title='{:,} member dengan role {}'.format(len(users), check_role.name), description=page, color=0XFF8C00)
        embed.set_footer(text='ROLE ID: {}\n{}#{}'.format(check_role.id, ctx.author.name, ctx.author.discriminator),
                         icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def rolecount(self, ctx):
        """Menghitung berapa banyak role dalam server. (termasuk @everyone)"""
        em = discord.Embed(color=0XFF8C00, description = "> Server *{}*\n> Memiliki total {} role".format(ctx.guild.name, len(ctx.guild.roles) - 1))
        em.set_author(name = "Total Role", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
        em.set_footer(text = "SERVER ID : {}\n{}#{}".format(ctx.guild.id, ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)

    @commands.command(pass_context=True)
    async def emptyroles(self, ctx):
        """Menampilkan list role yang tidak memiliki member atau role kosong."""

        check_roles = ctx.guild.roles # grab in hierarchy order so they're easier to find in the server settings
        rolecounts = self.role_accumulate(check_roles, ctx.guild.members) # same accumulate as the `roles` command

        sorted_list = []
        for role in check_roles:
            if role in rolecounts and rolecounts[role] == 0: # only add if count = 0
                sorted_list.append((role, rolecounts.get(role,0)))

        if not sorted_list: # another failsafe
            msg = 'Sepertinya tidak ada role yang kosong...'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        await self.rolelist_paginate(ctx, sorted_list, title='Role kosong')
