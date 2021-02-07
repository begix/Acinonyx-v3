import asyncio
import discord
import time
import random
import re
from   operator import itemgetter
from   discord.ext import commands
from   Cogs import Message
from   Cogs import Nullify
from   Cogs import DisplayName

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(XpBlock(bot, settings))

class XpBlock(commands.Cog):

    # Init with the bot reference, and a reference to the settings var and xp var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    @commands.command(pass_context=True)
    async def xpblock(self, ctx, *, user_or_role : str = None):
        """Menambahkan user atau role kedalam xp block list (admin only)."""

        em = discord.Embed(color = 0XFF8C00,description = "> Menambahkan user atau role kedalam xp block list\n> \n"
                                                          "> **Panduan**"
                                                          "> `{}xpblock [user/role]`"
                                                          .format(ctx.prefix))
        em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\n{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))

        # Check if we're suppressing @here and @everyone mentions
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        isAdmin = ctx.message.author.permissions_in(ctx.message.channel).administrator
        if not isAdmin:
            checkAdmin = self.settings.getServerStat(ctx.message.guild, "AdminArray")
            for role in ctx.message.author.roles:
                for aRole in checkAdmin:
                    # Get the role that corresponds to the id
                    if str(aRole['ID']) == str(role.id):
                        isAdmin = True
        # Only allow admins to change server stats
        if not isAdmin:
            msg = '┐(￣ヘ￣;)┌\nKamu tidak memiliki izin untuk menggunakan command ini.'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return

        if user_or_role == None:
            await ctx.message.channel.send(embed=em)
            return

        roleName = user_or_role
        is_user = True
        if type(user_or_role) is str:
            # Check user first
            user_or_role = DisplayName.memberForName(roleName, ctx.guild)
            if not user_or_role:
                is_user = False
                # Check role
                if roleName.lower() == "everyone" or roleName.lower() == "@everyone":
                    user_or_role = ctx.guild.default_role
                else:
                    user_or_role = DisplayName.roleForName(roleName, ctx.guild)
                    
            if not user_or_role:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(roleName)
                # Check for suppress
                if suppress:
                    msg = Nullify.clean(msg)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.message.channel.send(embed = em)
                return
        
        if is_user:
            # Check if they're admin or bot admin
            isAdmin = user_or_role.permissions_in(ctx.message.channel).administrator
            if not isAdmin:
                checkAdmin = self.settings.getServerStat(ctx.message.guild, "AdminArray")
                for role in user_or_role.roles:
                    for aRole in checkAdmin:
                        # Get the role that corresponds to the id
                        if str(aRole['ID']) == str(role.id):
                            isAdmin = True
            if isAdmin:
                msg = "┐(￣ヘ￣;)┌\nKamu tidak dapat menggunakan command ini kepada admin lain."
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)
                return
            ur_name = DisplayName.name(user_or_role)
        else:
            # Check if the role is admin or bot admin
            isAdmin = user_or_role.permissions.administrator
            if not isAdmin:
                checkAdmin = self.settings.getServerStat(ctx.message.guild, "AdminArray")
                for aRole in checkAdmin:
                    # Get the role that corresponds to the id
                    if str(aRole['ID']) == str(user_or_role.id):
                        isAdmin = True
            if isAdmin:
                msg = "┐(￣ヘ￣;)┌\nKamu tidak dapat menggunakan command ini kepada admin lain."
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)
                return

            ur_name = user_or_role.name

        # Now we see if we already have that role in our list
        promoArray = self.settings.getServerStat(ctx.message.guild, "XpBlockArray")

        for aRole in promoArray:
            # Get the role that corresponds to the id
            if str(aRole) == str(user_or_role.id):
                # We found it - throw an error message and return
                msg = '**{}** sudah didalam list.'.format(ur_name)
                # Check for suppress
                if suppress:
                    msg = Nullify.clean(msg)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.message.channel.send(embed = em)
                return

        # If we made it this far - then we can add it
        promoArray.append(user_or_role.id)
        self.settings.setServerStat(ctx.message.guild, "XpBlockArray", promoArray)

        msg = '**{}** ditambahkan kedalam list.'.format(ur_name)
        # Check for suppress
        if suppress:
            msg = Nullify.clean(msg)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.message.channel.send(embed = em)
        return
        
    
    @commands.command(pass_context=True)
    async def xpunblockall(self, ctx):
        """Menghapus semua user dan role yang terdarfat dalam blocklist (admin only)."""

        # Check if we're suppressing @here and @everyone mentions
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        isAdmin = ctx.message.author.permissions_in(ctx.message.channel).administrator
        if not isAdmin:
            checkAdmin = self.settings.getServerStat(ctx.message.guild, "AdminArray")
            for role in ctx.message.author.roles:
                for aRole in checkAdmin:
                    # Get the role that corresponds to the id
                    if str(aRole['ID']) == str(role.id):
                        isAdmin = True
        # Only allow admins to change server stats
        if not isAdmin:
            msg = '┐(￣ヘ￣;)┌\nKamu tidak memiliki hak untuk menggunakan command ini.'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return

        xparray = self.settings.getServerStat(ctx.message.guild, "XpBlockArray")
        self.settings.setServerStat(ctx.message.guild, "XpBlockArray", [])
        if len(xparray) == 1:
            msg = "*1* user/role telah diunblock dari system xp."
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.send(embed = em)
        else:
            msg = "*{}* user/role telah diunblock dari system xp.".format(len(xparray))
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.send(embed = em)


    @commands.command(pass_context=True)
    async def xpunblock(self, ctx, *, user_or_role : str = None):
        """Menghapus user atau role dari list xp block (admin only)."""
        em = discord.Embed(color = 0XFF8C00,description = "> Menghapus user atau role dari list xp block\n> \n"
                                                          "> **Panduan**"
                                                          "> `{}xpunblock [user/role]`"
                                                          .format(ctx.prefix))
        em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))

        # Check if we're suppressing @here and @everyone mentions
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        isAdmin = ctx.message.author.permissions_in(ctx.message.channel).administrator
        if not isAdmin:
            checkAdmin = self.settings.getServerStat(ctx.message.guild, "AdminArray")
            for role in ctx.message.author.roles:
                for aRole in checkAdmin:
                    # Get the role that corresponds to the id
                    if str(aRole['ID']) == str(role.id):
                        isAdmin = True
        # Only allow admins to change server stats
        if not isAdmin:
            msg = '┐(￣ヘ￣;)┌\nKamu tidak memiliki izin untuk menggunakan command ini.'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return

        if user_or_role == None:
            await ctx.message.channel.send(embed = em)
            return

        roleName = user_or_role
        is_user = True
        if type(user_or_role) is str:
            # Check user first
            user_or_role = DisplayName.memberForName(roleName, ctx.guild)
            if not user_or_role:
                is_user = False
                # Check role
                if roleName.lower() == "everyone" or roleName.lower() == "@everyone":
                    user_or_role = ctx.guild.default_role
                else:
                    user_or_role = DisplayName.roleForName(roleName, ctx.guild)
                    
            if not user_or_role:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(roleName)
                # Check for suppress
                if suppress:
                    msg = Nullify.clean(msg)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.message.channel.send(embed = em)
                return
        
        if is_user:
            ur_name = DisplayName.name(user_or_role)
        else:
            ur_name = user_or_role.name

        # If we're here - then the role is a real one
        promoArray = self.settings.getServerStat(ctx.message.guild, "XpBlockArray")

        for aRole in promoArray:
            # Check for Name
            if str(aRole) == str(user_or_role.id):
                # We found it - let's remove it
                promoArray.remove(aRole)
                self.settings.setServerStat(ctx.message.guild, "XpBlockArray", promoArray)
                msg = '**{}** berhasil dihapus dari xp block list.'.format(ur_name)
                # Check for suppress
                if suppress:
                    msg = Nullify.clean(msg)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.message.channel.send(embed = em)
                return

        # If we made it this far - then we didn't find it
        msg = '┐(￣ヘ￣;)┌\n**{}** tidak ada dalam xp block list ku.'.format(ur_name)
        # Check for suppress
        if suppress:
            msg = Nullify.clean(msg)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.message.channel.send(embed = em)


    @commands.command(pass_context=True)
    async def listxpblock(self, ctx):
        """Melihat semua user/role dari list xp block."""

        # Check if we're suppressing @here and @everyone mentions
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        promoArray = self.settings.getServerStat(ctx.message.guild, "XpBlockArray")
        
        # rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
        
        #promoSorted = sorted(promoArray, key=itemgetter('Name'))

        if not len(promoArray):
            em = discord.Embed(color = 0XFF8C00, description = "> ┐(￣ヘ￣;)┌\n"
                                                               "> Tidak ada user atau role yang di blokir.\n"
                                                               "> Gunakan command `{}xpblock [user/role]` untuk menambahkan kedaftar list xp block")
            em.set_author(name = "listxpblock command", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_thumbnail(url = "{}".format(ctx.message.guild.icon_url))
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return
        
        roleText = "__**Daftar blokir user dan role saat ini:**__\n\n"
        
        for arole in promoArray:
            test = DisplayName.memberForID(arole, ctx.guild)
            if test:
                # It's a user
                roleText = roleText + "**{}**, ".format(DisplayName.name(test))
                continue
            test = DisplayName.roleForID(arole, ctx.guild)
            if test:
                # It's a role
                roleText = roleText + "**{}** (Role), ".format(test.name)
                continue
            # Didn't find a role or person
            roleText = roleText + "**{}** (dihapus dari server), ".format(arole)

        roleText = roleText[:-2]
        # Check for suppress
        if suppress:
            roleText = Nullify.clean(roleText)
        em = discord.Embed(color = 0XFF8C00, description = roleText)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.channel.send(embed = em)