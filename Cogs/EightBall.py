import asyncio
import discord
import random
from   discord.ext import commands
from   Cogs import Settings

def setup(bot):
    # Add the bot
    bot.add_cog(EightBall(bot))

class EightBall(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(hidden=True)
    # async def lmap(self, ctx, *, question = None):
    #     """Let me ask Pooter..."""

    #     await ctx.invoke(self.eightball,question=question)

    @commands.command(pass_context=True)
    async def eightball(self, ctx, *, question = None):
        """Tanya apa kau?!."""

        if question == None:
            msg = 'You need to ask me a question first.'
            await ctx.channel.send(msg)
            return

        answerList = [  "(⇀‸↼‶)\nBodo amat ahh...",
                        "┐(︶▽︶)┌\nSepertinya sih begitu",
                        "─=≡Σ((( つ＞＜)つ\nGak usah ragu-ragu",
                        "(*￣▽￣)b\nYaa, Tentu saja Broo~",
                        "(•ิ_•ิ)?\nKamu mungkin bergantung padanya",
                        "(b ᵔ▽ᵔ)b\nAhh aku mengerti, Yaa!",
                        "(￣ー￣;)ゞ\nKayaknya sih begitu",
                        "(≧▽≦)\nBagus juga",
                        "(≧▽≦)\nYaa~!",
                        "(_　_|||)\nIyaa-iyaa",
                        "┐(￣ヘ￣;)┌\nGak tau lagi aku mau ngomong apa bro",
                        "(¯ ¯٥)\nTanya lagi nanti yaa",
                        "╮(￣ω￣;)╭\nMungkin aku tidak akan mengatakannya sekarang ",
                        "╮(￣ω￣;)╭\nAku nggk bisa memperkirakannya bro",
                        "（；￣д￣)\nPikir aja sendiri..",
                        "(*>ω<)b\nOdading mang oleh Mantap",
                        "(￣ー￣;)ゞ\nKau pikir saja sendiri!"
                        ]
        randnum = random.randint(0, len(answerList)-1)
        msg = '{}'.format(answerList[randnum])
        # Say message
        await ctx.channel.send(msg)
