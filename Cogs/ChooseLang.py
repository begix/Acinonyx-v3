import discord
from   discord.ext import commands
from   Cogs        import DisplayName
from   Cogs        import Settings

def setup(bot):
    # Menambahkan bot
    settings = bot.get_cog("Settings")
    bot.add_cog(ChooseLang(bot, settings))

class ChooseLang(commands.Cog):

    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")


    @commands.command(pass_context = True)
    async def lang(self, ctx):
        cekAuthor = ctx.author
        checkLang = self.settings.getUserStat(cekAuthor, ctx.guild, "Language")

        if checkLang == "ID":
            msg  = "(￣▽￣)ノ Haii~\n"
            msg += "Kamu telah mengatur bahasa Indonesia untuk bot ini.\n"
            msg += "Ketik `clear` untuk menghapus bahasa yang telah kamu pilih"

            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))

            msgFirst = await ctx.send(embed = em)
            confirm = ["clear"]
            try:
                msg = await self.bot.wait_for('message', timeout=15, check=lambda msg: msg.author == ctx.author)
            except:
                msg  = "(￣▽￣)ノ Haii~\n"
                msg += "Kamu telah mengatur bahasa Indonesia untuk bot ini."

                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
                return await msgFirst.edit(embed = em)
            message = str(msg.content.lower())

            if message not in confirm and message not in ["clear"]:
                msg  = "(￣▽￣)ノ Haii~\n"
                msg += "Kamu telah mengatur bahasa Indonesia untuk bot ini."

                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author),
                              icon_url = "{}".format(ctx.author.avatar_url))
                return await msgFirst.edit(embed = em)

            await msgFirst.delete()

            self.settings.setUserStat(ctx.author, ctx.guild, "Language", None)

            msg  = "<:indonesia:798977282886467635> **INDONESIA**\n"
            msg += "Kamu telah menghapus bahasa untuk bot ini\n"
            msg += "Silahkan ketik `{}lang` untuk memilih bahasa dalam bot ini\n\n".format(ctx.prefix)
            msg += "<:English:798978134711599125> **ENGLISH**\n"
            msg += "You have deleted the language for this bot\n"
            msg += "Type `{}lang` to select the language in this bot".format(ctx.prefix)

            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        if checkLang == "EN":
            msg  = "(￣▽￣)ノ Haii~\n"
            msg += "You have set the English language for this bot.\n"
            msg += "Type `clear` to delete the language you have selected"

            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
            msgFirst = await ctx.send(embed = em)
            confirm = ["clear"]
            try:
                msg = await self.bot.wait_for('message', timeout=15, check=lambda msg: msg.author == ctx.author)
            except:
                msg  = "(￣▽￣)ノ Haii~\n"
                msg += "You have set the English language for this bot."

                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
                return await msgFirst.edit(embed = em)
            message = str(msg.content.lower())

            if message not in confirm and message not in ["clear"]:
                msg  = "(￣▽￣)ノ Haii~\n"
                msg += "You have set the English language for this bot."

                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}".format(ctx.author),
                              icon_url = "{}".format(ctx.author.avatar_url))
                return await msgFirst.edit(embed = em)

            await msgFirst.delete()

            self.settings.setUserStat(ctx.author, ctx.guild, "Language", None)

            msg  = "<:indonesia:798977282886467635> **INDONESIA**\n"
            msg += "Kamu telah menghapus bahasa untuk bot ini\n"
            msg += "Silahkan ketik `{}lang` untuk memilih bahasa dalam bot ini\n\n".format(ctx.prefix)
            msg += "<:English:798978134711599125> **ENGLISH**\n"
            msg += "You have deleted the language for this bot\n"
            msg += "Type `{}lang` to select the language in this bot".format(ctx.prefix)
            
            em = discord.Embed(color = 0XFF8C00, description = msg)
            em.set_footer(text = "{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        msg  = "<:indonesia:798977282886467635> **INDONESIA**\n"
        msg += "Kamu belum mengatur bahasa untuk bot ini.\n\n"
        msg += "<:English:798978134711599125> **ENGLISH**\n"
        msg += "You haven't set the language for this bot.\n\n"
        msg += "*Pilih dibawah ini / Select it below*"

        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}".format(ctx.author),
                      icon_url = "{}".format(ctx.author.avatar_url))
        msg = await ctx.send(embed = em, delete_after = 15)
        await msg.add_reaction('<:indonesia:798977282886467635>')
        await msg.add_reaction('<:English:798978134711599125>')

        while True:
            try:
                reaction, user = await self.bot.wait_for(event='reaction_add',)
                if user == ctx.author:
                    emoji = str(reaction.emoji)
                    if emoji == '<:indonesia:798977282886467635>':
                        await msg.delete()

                        member = ctx.author
                        self.settings.setUserStat(member, ctx.guild, "Language", "ID")

                        msg  = "o(>ω<)o Horeeee~!\n"
                        msg += "Kamu telah mengatur bot ini dengan bahasa indonesia.\n"
                        msg += "Silahkan ulangi command yang baru saja kamu gunakan."
                        em = discord.Embed(color = 0XFF8C00, description = msg)
                        em.set_footer(text = "{}".format(ctx.author),
                                      icon_url = "{}".format(ctx.author.avatar_url))
                        await ctx.send(embed = em)

                    if emoji == '<:English:798978134711599125>':
                        await msg.delete()

                        member = ctx.author
                        self.settings.setUserStat(member, ctx.guild, "Language", "EN")

                        msg  = "o(>ω<)o Yaaaaay~!\n"
                        msg += "You have configured this bot in English.\n"
                        msg += "Please repeat the command that you just used."
                        em = discord.Embed(color = 0XFF8C00, description = msg)
                        em.set_footer(text = "{}".format(ctx.author),
                                      icon_url = "{}".format(ctx.author.avatar_url))
                        await ctx.send(embed = em)
            except Exception as e:
                await msg.send("```\n{}\n```".format(e))