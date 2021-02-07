import asyncio, discord, re
from   discord.ext import commands
from   Cogs import Nullify

# bot = None
# url_regex = re.compile(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")

def setup(bot):
    # This module isn't actually a cog - but it is a place
    # we can call "a trash fire"
    bot.add_cog(Utils(bot))
    # global bot
    # bot = bot_start

class Utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.url_regex = re.compile(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")

    def suppressed(self,ctx,msg):
        # Checks if the passed server is suppressing @here and @everyone and adjust the msg accordingly
        guild = ctx if isinstance(ctx,discord.Guild) else ctx.guild if isinstance(ctx,discord.ext.commands.Context) else None
        if not guild: return msg
        settings = self.bot.get_cog("Settings")
        if not settings: return msg
        return Nullify.clean(msg) if settings.getServerStat(guild, "SuppressMentions", True) else msg

    def is_owner(self,ctx,member=None):
        # Checks if the user in the passed context is an owner
        settings = self.bot.get_cog("Settings")
        if not settings: return False
        member = ctx.author if not member else member
        return settings.isOwner(member)

    def is_admin(self,ctx,member=None):
        # Checks if the user in the passed context is admin
        member = ctx.author if not member else member
        return member.permissions_in(ctx.channel).administrator

    def is_bot_admin_only(self,ctx,member=None):
        # Checks only if we're bot admin
        settings = self.bot.get_cog("Settings")
        if not settings: return False
        member = ctx.author if not member else member
        if not hasattr(member,"roles"): return False # No roles to iterate - can't be bot admin
        return any(role for role in member.roles for check in settings.getServerStat(ctx.guild, "AdminArray", []) if str(role.id) == str(check["ID"]))

    def is_bot_admin(self,ctx,member=None):
        # Checks if the user in the passed context is admin or bot admin
        member = ctx.author if not member else member
        return member.permissions_in(ctx.channel).administrator or self.is_bot_admin_only(ctx,member)

    async def is_owner_reply(self,ctx,member=None,not_claimed="...",not_owner="┐(￣ヘ￣;)┌\nKamu bukan owner ku"):
        # Auto-replies if the user isn't an owner
        are_we = self.is_owner(ctx,member)
        if are_we == None: await ctx.send(not_claimed)
        elif are_we == False: 
            em = discord.Embed(color = 0XFF8C00, description = not_owner)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url)) 
            await ctx.send(embed = em)
        return are_we

    async def is_admin_reply(self,ctx,member=None,message="┐(￣ヘ￣;)┌\nKamu tidak memiliki izin untuk menggunakan command ini.",message_when=False):
        # Auto-replies if the user doesn't have admin privs
        are_we = self.is_admin(ctx,member)
        em = discord.Embed(color = 0XFF8C00, description = message)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url)) 
        if are_we == message_when:
            em = discord.Embed(color = 0XFF8C00, description = message)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url)) 
            await ctx.send(embed = em)
        return are_we

    async def is_bot_admin_only_reply(self,ctx,member=None,message="┐(￣ヘ￣;)┌\nKamu tidak memiliki izin untuk menggunakan command ini.",message_when=False):
        # Auto-replies if the user doesn't have admin or bot admin privs
        are_we = self.is_bot_admin_only(ctx,member)
        em = discord.Embed(color = 0XFF8C00, description = message)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        if are_we == message_when:
            em = discord.Embed(color = 0XFF8C00, description = message)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url)) 
            await ctx.send(embed = em)
        return are_we

    async def is_bot_admin_reply(self,ctx,member=None,message="┐(￣ヘ￣;)┌\nKamu tidak memiliki izin untuk menggunakan command ini.",message_when=False):
        # Auto-replies if the user doesn't have admin or bot admin privs
        are_we = self.is_bot_admin(ctx,member)
        em = discord.Embed(color = 0XFF8C00, description = message)
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        if are_we == message_when:
            em = discord.Embed(color = 0XFF8C00, description = message)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url)) 
            await ctx.send(embed = em)
        return are_we

    def yes_no_setting(self,ctx,display_name,setting_name,yes_no=None,default=None,is_global=False):
        # Get or set a true/false value and return the resulting message
        guild = ctx if isinstance(ctx,discord.Guild) else ctx.guild if isinstance(ctx,discord.ext.commands.Context) else None
        if not guild and not is_global: return "Aku tidak dapat mendapatkan server dari sini :("
        settings = self.bot.get_cog("Settings")
        if not settings: return "Sepertinya ada yang salah dengan module ku :("
        current = settings.getGlobalStat(setting_name, default) if is_global else settings.getServerStat(guild, setting_name, default)
        if yes_no == None:
            # Output what we have
            return "{} saat ini *{}*.".format(display_name,"dinyalakan" if current else "dimatikan")
        elif yes_no.lower() in [ "yes", "on", "true", "dinyalakan", "dinyalakan" ]:
            yes_no = True
            msg = "{} {} *dinyalakan*.".format(display_name,"masih tetap" if current else "saat ini")
        elif yes_no.lower() in [ "no", "off", "false", "dimatikan", "dimatikan" ]:
            yes_no = False
            msg = "{} {} *dimatikan*.".format(display_name,"saat ini" if current else "masih tetap")
        else:
            msg = "Kamu memasukan settingan yang salah."
            yes_no = current
        if not yes_no == current:
            if is_global: settings.setGlobalStat(setting_name, yes_no)
            else: settings.setServerStat(ctx.guild, setting_name, yes_no)
        return msg

    def get_urls(self,message):
        # Returns a list of valid urls from a passed message/context/string
        message = message.content if isinstance(message,discord.Message) else message.message.content if isinstance(message,discord.ext.commands.Context) else str(message)
        return [x.group(0) for x in re.finditer(self.url_regex,message)]