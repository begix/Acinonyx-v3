import discord
import ast
from discord.ext import commands
from Cogs import Utils
from Cogs import Settings
from Cogs import DisplayName
from Cogs import Time
from Cogs import DL
from Cogs import ComicHelper
from Cogs import TinyURL
from Cogs import CheckRoles
from Cogs import UserTime
from Cogs import GetImage
from Cogs import Nullify
from Cogs import PCPP
from Cogs import ProgressBar
from Cogs import Monitor
from Cogs import Message
from Cogs import FuzzySearch
from Cogs import ReadableTime
from Cogs import Setup

osuKey = "526d85b33ad4b0912850229a00e17e91b612d653"

def setup(bot):
    settings = bot.get_cog("Settings")
    bot.add_cog(Eval(bot, settings))

def insert_returns(body):
# insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Eval(commands.Cog):

    def __init__(self, bot, settings):
        self.bot = bot
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")
        Settings = self.bot.get_cog("Settings")
        Time = self.bot.get_cog("Time")
        DL = self.bot.get_cog("DL")
        ComicHelper = self.bot.get_cog("ComicHelper")
        TinyURL = self.bot.get_cog("TinyURL")
        CheckRoles = self.bot.get_cog("CheckRoles")
        UserTime = self.bot.get_cog("UserTime")
        GetImage = self.bot.get_cog("GetImage")
        Nullify = self.bot.get_cog("Nullify")
        PCPP = self.bot.get_cog("PCPP")
        ProgressBar = self.bot.get_cog("ProgressBar")
        Monitor = self.bot.get_cog("Monitor")
        Message = self.bot.get_cog("Message")
        FuzzySearch = self.bot.get_cog("FuzzySearch")
        ReadableTime = self.bot.get_cog("ReadableTime")
        Setup = self.bot.get_cog("Setup")
        self.settings = settings
        osuKey = "526d85b33ad4b0912850229a00e17e91b612d653"


    @commands.command()
    async def eval(self, ctx, *, cmd):
      """Evaluates input. (Owner-only)
      Usable globals:
      - `bot`       : bot instance
      - `discord`   : discord module
      - `commands`  : discord.ext.commands module
      - `ctx`       : invokation context
      - `self`      : instance class
      - `__import__`: builtin `__import__` function
      """
      try:
        isOwner = self.settings.isOwner(ctx.author)
        if isOwner == False:
            msg = "Hus hus!!\nJangan main main sama command ini"
            em = discord.Embed(description = msg)
            return await ctx.send(embed = em)

        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            'self': self,
            'DisplayName' : DisplayName,
            'osuKey': "526d85b33ad4b0912850229a00e17e91b612d653",
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send("```\n{}\n```".format(result))
      except Exception as e:
        await ctx.send("```\n{}\n```".format(e))