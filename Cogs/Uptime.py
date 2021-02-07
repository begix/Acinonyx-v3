import asyncio
import discord
import time
from   operator import itemgetter
from   discord.ext import commands
from   Cogs import ReadableTime

def setup(bot):
    # Add the bot
    bot.add_cog(Uptime(bot))

# This is the Uptime module. It keeps track of how long the bot's been up

class Uptime(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot
        self.startTime = int(time.time())

    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        """Melihat uptime bot."""
        currentTime = int(time.time())
        timeString  = ReadableTime.getReadableTimeBetween(self.startTime, currentTime)
        msg = 'Aku telah online selama\n*{}*.'.format(timeString)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author))
        await ctx.channel.send(embed = em)