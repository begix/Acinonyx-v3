import asyncio
import discord
import os
import time
from   datetime import datetime
from   discord.ext import commands

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(RateLimit(bot, settings))

# This is the RateLimit module. It keeps users from being able to spam commands

class RateLimit(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.commandCooldown = 5 # 5 seconds between commands - placeholder, overridden by settings
        self.maxCooldown = 10 # 10 seconds MAX between commands for cooldown
        
    def canRun( self, firstTime, threshold ):
        # Check if enough time has passed since the last command to run another
        currentTime = int(time.time())
        if currentTime > (int(firstTime) + int(threshold)):
            return True
        else:
            return False
        
    async def test_message(self, message):
        # Implemented to bypass having this called twice
        return { "Ignore" : False, "Delete" : False }

    async def message(self, message):
        # Check the message and see if we should allow it - always yes.
        # This module doesn't need to cancel messages - but may need to ignore
        ignore = False

        # Get current delay
        currDelay = self.settings.getGlobalStat("CommandCooldown",self.commandCooldown)
        
        # Check if we can run commands
        try:
            lastTime = int(self.settings.getUserStat(message.author, message.guild, "LastCommand"))
        except:
            # Not set - or incorrectly set - default to 0
            lastTime = 0
        # None fix
        if lastTime == None:
            lastTime = 0
        if not self.canRun( lastTime, currDelay ):
            # We can't run commands yet - ignore
            ignore = True
        
        return { 'Ignore' : ignore, 'Delete' : False }
        
    async def oncommand(self, ctx):
        # Let's grab the user who had a completed command - and set the timestamp
        self.settings.setUserStat(ctx.message.author, ctx.message.guild, "LastCommand", int(time.time()))


    @commands.command(pass_context=True)
    async def ccooldown(self, ctx, delay : int = None):
        """Mengatur cooldown untuk semua command (owner only)."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild

        # Only allow owner
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == None:
            return
        elif isOwner == False:
            msgText = ["Hus hus, jangan main main sama command ini",
                       "Command ini bahaya loh dek, jangan main main!",]
            msg = random.choice(msgText)
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.send(embed = em)
            return

        # Get current delay
        currDelay = self.settings.getGlobalStat("CommandCooldown",self.commandCooldown)
        
        if delay == None:
            if currDelay == 1:
                msg = 'Cooldown untuk semua command telah dirubah menjadi *1 Detik*'
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.channel.send(embed = em)
            else:
                msg = 'Cooldown untuk semua command telah dirubah menjadi *{} Detik.*'.format(currDelay)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.channel.send(embed = em)
            return
        
        try:
            delay = int(delay)
        except Exception:
            msg = 'Cooldown harus berupa angka.'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return
        
        if delay < 0:
            msg = 'Cooldown harus lebih dari *0 detik*.'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return

        if delay > self.maxCooldown:
            if self.maxCooldown == 1:
                msg = 'Cooldown tidak dapat lebih dari *1 detik*.'
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.channel.send(embed = em)
            else:
                msg = 'Cooldown tidak dapat lebih dari *{} detik*.'.format(self.maxCooldown)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.channel.send(embed = em)
            return
        
        self.settings.setGlobalStat("CommandCooldown",delay)
        if delay == 1:
            msg = 'Cooldown untuk semua command telah dirubah menjadi *1 Detik*.*'
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
        else:
            msg = 'Cooldown untuk semua command telah dirubah menjadi *{} Detik.*'.format(delay)
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
