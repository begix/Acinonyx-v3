import discord
import time
from datetime    import datetime
from discord.ext import commands
from Cogs        import Utils, GetImage, Message, DisplayName, Nullify

def setup(bot):
    settings = bot.get_cog("Settings")
    bot.add_cog(ImageFilter(bot, settings))

class ImageFilter(commands.Cog):
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global DisplayName
        DisplayName = self.bot.get_cog("DisplayName")

    def canDisplay(self, server):
        lastTime  = int(self.settings.getServerStat(server, "LastPicture", 0))
        threshold = int(self.settings.getServerStat(server, "PictureTherehold", 0))
        if not GetImage.canDisplay( lastTime, threshold ):
            return False
        self.settings.getServerStat(server, "LastPicture", int(time.time()))
        return True

    async def _image_do(self, ctx, filters, avatar):
        ImageAPI = "https://some-random-api.ml/canvas/{}/?avatar={}".format(filters, avatar)
        if not self.canDisplay(ctx.guild): return
        if filters == "triggered":
            await ctx.send(ImageAPI)
            return
        return await Message.Embed(
            description = "**[IMAGE URL]({})**".format(ImageAPI),
            image = ImageAPI, 
            color = 0XFF8C00,
            footer = "{} Filter\nPowered by: Some Random Api\n{}".format(filters.capitalize(), ctx.author),
            footer_icon = "{}".format(ctx.author.avatar_url)).send(ctx)

    @commands.command(pass_context=True)
    async def greyscale(self, ctx, *,member = None):
        """Filter avatar greyscale"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", ImageAPI = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "greyscale", avatar)

    @commands.command(pass_context=True)
    async def invert(self, ctx, *,member = None):
        """Filter avatar invert

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "invert", avatar)

    @commands.command(pass_context=True)
    async def brightness(self, ctx, *,member = None):
        """Filter avatar brightness

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "brightness", avatar) 
        
    @commands.command(pass_context=True)
    async def threshold(self, ctx, *,member = None):
        """Filter avatar threshold

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "threshold", avatar)

    @commands.command(pass_context=True)
    async def sepia(self, ctx, *,member = None):
        """Filter avatar sepia

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "sepia", avatar)

    @commands.command(pass_context=True)
    async def red(self, ctx, *,member = None):
        """Filter avatar red

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "red", avatar)

    @commands.command(pass_context=True)
    async def green(self, ctx, *,member = None):
        """Filter avatar green

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "green", avatar)

    @commands.command(pass_context=True)
    async def blue(self, ctx, *,member = None):
        """Filter avatar blue

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "blue", avatar)

    @commands.command(pass_context=True)
    async def blurple(self, ctx, *,member = None):
        """Filter avatar blurple

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "blurple", avatar)

    @commands.command(pass_context=True)
    async def pixelate(self, ctx, *,member = None):
        """Filter avatar pixelate

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "pixelate", avatar)

    @commands.command(pass_context=True)
    async def blur(self, ctx, *,member = None):
        """Filter avatar blur

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "blur", avatar)

    @commands.command(pass_context=True)
    async def triggered(self, ctx, *,member = None):
        """Triggered effect

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "triggered", avatar)

    @commands.command(pass_context=True)
    async def glass(self, ctx, *,member = None):
        """Filter avatar glass

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "glass", avatar)

    @commands.command(pass_context=True)
    async def wasted(self, ctx, *,member = None):
        """Wasted effect

        member dapat berupa:
        (optional)
        • mention
        • username / nickname"""
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False

        if member == None:
            member = ctx.author
        
        if type(member) is str:
            memberName = member
            new_mem = DisplayName.memberForName(memberName, ctx.message.guild)
            if not new_mem:
                msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.message.channel.send(embed = em)
                return
            member = new_mem
        avatar = member.avatar_url_as(format = "png", size = 512)
        if not len(avatar):
            avatar = member.default_avatar_url
        await self._image_do(ctx, "wasted", avatar)