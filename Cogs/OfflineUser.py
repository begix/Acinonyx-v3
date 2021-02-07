import asyncio, discord
from   discord.ext import commands
from   Cogs import Utils, DisplayName

def setup(bot):
    # Add the bot
    bot.add_cog(OfflineUser(bot))

# This is the OfflineUser module

class OfflineUser(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot
        self.settings = bot.get_cog("Settings")
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")
        
    async def _send_message(self, ctx, msg, pm = False):
        # Helper method to send messages to their proper location
        if pm == True and not ctx.channel == ctx.author.dm_channel:
            # Try to dm
            try:
                em = discord.Embed(color = 0XFF8C00, description = msg)
                await ctx.author.send(embed = em)
                return await ctx.message.add_reaction("📬")
            except discord.Forbidden:
                pass
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if not self.settings.getServerStat(message.guild, "RemindOffline"):
            return
        # Valid message
        ctx = await self.bot.get_context(message)
        if ctx.command:
            # Don't check if we're running a command
            return
        if not len(message.mentions):
            return
        name_list = [DisplayName.name(x) for x in message.mentions if x.status is discord.Status.offline]
        if not len(name_list):
            # No one was offline
            return
        if len(name_list) == 1:
            msg = "{}\nsepertinya {} sedang offline\nSilahkan private chat ke dia jika kamu memiliki urusan penting.".format(ctx.author.mention, name_list[0])
        else:
            msg = "{}, sepertinya salah satu dari member yang kamu mention sedang offline\nPM mereka jika darurat:\n{}".format(ctx.author.mention, ", ".join(name_list))
        await self._send_message(ctx, msg, True)

    @commands.command(pass_context=True)
    async def remindoffline(self, ctx, *, yes_no = None):
        """Menyalakan pengingat offline user(admin server only).
        
        Jika fitur ini dinyalakan dalam server, saat ada user mention user lain yang sedang offline,
        aku akan mengingatkan mereka lewat pesan DM bahwa orang yang dituju sedang offline"""
        if not await Utils.is_bot_admin_reply(ctx): return
        msg = Utils.yes_no_setting(ctx,"Offline user reminder","RemindOffline",yes_no)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)