import discord
from discord.ext import commands
from Cogs import Utils, Settings
from enum import Enum
import requests, json, re, random, base64, subprocess

def setup(bot):
    settings = bot.get_cog("Settings")
    bot.add_cog(Osu(bot, settings))


class Osu(commands.Cog):

    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    # @commands.command()
    # async def osuprint(self, ctx, player = None):
    #     """Print out json api osu(Owner-only)"""
    #     isOwner = self.settings.isOwner(ctx.author)
    #     if isOwner == False:
    #         msg = "Siapa yaa?"
    #         em = discord.Embed(description = msg)
    #         return await ctx.send(embed = em)

    #     playerCheck = requests.get("https://osu.ppy.sh/api/get_user_recent?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}&m=0&limit=1".format(player))
    #     data = playerCheck.text
    #     data = json.loads(data)
    #     dataPlayer = data
    #     await ctx.send("```\n{}\n```".format(dataPlayer))

    @commands.command()
    async def setosu(self, ctx, *, player = None):
        """**INDONESIA**
        Set Osu!Player mu dalam server ini.
        
        **ENGLISH**
        Set your Osu!Player in this server
        
        Contoh / Example:
        acx setosu kazereborn"""
        checkData = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if checkData is not None:
          try:
            playerCheck = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}".format(checkData))
            data = playerCheck.text
            data = json.loads(data)
            dataPlayer = data
            userId = dataPlayer[0]["user_id"]
            username = dataPlayer[0]["username"]

            if LangCheck == "ID":
                msg =  "Osu player kamu dalam server ini\n"
                msg += "*Player : {}*\n".format(username)
                msg += "*Id : {}*\n\n".format(userId)
                msg += "Ketik *`ya`* untuk menghapus player osu kamu"
                em = discord.Embed(color = 0XFF8C00,
                                   description = msg)
                em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                em.add_field(name = "**HOMEPAGE**",
                             value = "https://osu.ppy.sh/users/{}".format(userId))
                em.set_footer(text = "{}".format(ctx.author),
                              icon_url = "{}".format(ctx.author.avatar_url))
                Msg = await ctx.send(embed = em)
                confirm = ['ya']
                try:
                    msg = await self.bot.wait_for('message', timeout=15, check=lambda msg: msg.author == ctx.author)
                except:
                    msg =  "Osu player kamu dalam server ini\n"
                    msg += "*Player : {}*\n".format(username)
                    msg += "*Id : {}*".format(userId)
                    em = discord.Embed(color = 0XFF8C00, description = msg)
                    em.add_field(name = "**HOMEPAGE**",
                                 value = "https://osu.ppy.sh/users/{}".format(userId))
                    em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                    em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                                  icon_url = "{}".format(ctx.author.avatar_url))
                    return await Msg.edit(embed = em)
                message = str(msg.content.lower())

                if message not in confirm and message not in ['ya']:
                    msgDone =  "Osu player kamu dalam server ini\n"
                    msgDone += "*Player : {}*\n".format(username)
                    msgDone += "*Id : {}*".format(userId)
                    em = discord.Embed(color = 0XFF8C00, description = msgDone)
                    em.add_field(name = "**HOMEPAGE**",
                                value = "https://osu.ppy.sh/users/{}".format(userId))
                    em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                    em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                                  icon_url = "{}".format(ctx.author.avatar_url))
                    return await Msg.edit(embed = em)

                await Msg.delete()
                msg =  "Kamu telah manghapus Player Osu diserver ini.\n"
                msg += "Silahkan ketik *`{}setosu [player]`* untuk mengatur Osu player mu kembali".format(ctx.prefix)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                              icon_url = "{}".format(ctx.author.avatar_url))
                self.settings.setUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer", None)
                return await ctx.send(embed = em)

            if LangCheck == "EN":
                msg =  "Your Osu!Player in this server is\n"
                msg += "*Player : {}*\n".format(username)
                msg += "*Id : {}*\n\n".format(userId)
                msg += "Type *`clear`* to delete your Osu!Player in this server."
                em = discord.Embed(color = 0XFF8C00,
                                   description = msg)
                em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                em.add_field(name = "**HOMEPAGE**",
                             value = "https://osu.ppy.sh/users/{}".format(userId))
                em.set_footer(text = "{}".format(ctx.author),
                              icon_url = "{}".format(ctx.author.avatar_url))
                Msg = await ctx.send(embed = em)
                confirm = ['clear']
                try:
                    msg = await self.bot.wait_for('message', timeout=15, check=lambda msg: msg.author == ctx.author)
                except:
                    msg =  "Your Osu!Player in this server is\n"
                    msg += "*Player : {}*\n".format(username)
                    msg += "*Id : {}*".format(userId)
                    em = discord.Embed(color = 0XFF8C00, description = msg)
                    em.add_field(name = "**HOMEPAGE**",
                                 value = "https://osu.ppy.sh/users/{}".format(userId))
                    em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                    em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                                  icon_url = "{}".format(ctx.author.avatar_url))
                    return await Msg.edit(embed = em)
                message = str(msg.content.lower())

                if message not in confirm and message not in ['clear']:
                    msgDone =  "Your Osu!Player in this server is\n"
                    msgDone += "*Player : {}*\n".format(username)
                    msgDone += "*Id : {}*".format(userId)
                    em = discord.Embed(color = 0XFF8C00, description = msgDone)
                    em.add_field(name = "**HOMEPAGE**",
                                value = "https://osu.ppy.sh/users/{}".format(userId))
                    em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                    em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                                  icon_url = "{}".format(ctx.author.avatar_url))
                    return await Msg.edit(embed = em)

                await Msg.delete()
                msg =  "You have deleted your Osu!Player in this server.\n"
                msg += "Please type *`{}setosu [player]`* to set your Osu!Player in this server.".format(ctx.prefix)
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                              icon_url = "{}".format(ctx.author.avatar_url))
                self.settings.setUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer", None)
                return await ctx.send(embed = em)

          except Exception as e:
            print (e)
            if LangCheck == "ID":
                msg = "┐(￣ヘ￣;)┌\nPlayer yang kamu masukan tidak terdaftar."
                em = discord.Embed(color = 0XFF8C00,
                                   description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)

            if LangCheck == "ID":
                msg = "┐(￣ヘ￣;)┌\nLooks like player that you entered is not registered."
                em = discord.Embed(color = 0XFF8C00,
                                   description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)
        
        try:
          if player == None:
            return await self.player_not_found(ctx)
            
          try:
            if LangCheck == "ID":
                playerCheck = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}".format(player))
                data = playerCheck.text
                data = json.loads(data)
                dataPlayer = data
                userId = dataPlayer[0]["user_id"]
                username = dataPlayer[0]["username"]
                self.settings.setUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer", userId)
                msg =  "Kamu telah mengatur osu player untuk server ini\n"
                msg += "*Player : {}*\n".format(username)
                msg += "*ID : {}*".format(userId)
                em = discord.Embed(color = 0XFF8C00,
                                   description = "{}".format(msg))
                em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                em.add_field(name = "**HOMEPAGE**",
                             value = "https://osu.ppy.sh/users/{}".format(userId))
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)

            if LangCheck == "EN":
                playerCheck = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}".format(player))
                data = playerCheck.text
                data = json.loads(data)
                dataPlayer = data
                userId = dataPlayer[0]["user_id"]
                username = dataPlayer[0]["username"]
                self.settings.setUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer", userId)
                msg =  "You have set your Osu!Player for this server.\n"
                msg += "*Player : {}*\n".format(username)
                msg += "*ID : {}*".format(userId)
                em = discord.Embed(color = 0XFF8C00,
                                   description = "{}".format(msg))
                em.set_thumbnail(url = "http://s.ppy.sh/a/{}".format(userId))
                em.add_field(name = "**HOMEPAGE**",
                             value = "https://osu.ppy.sh/users/{}".format(userId))
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)
          except Exception as e:
            if LangCheck == "ID":
                msg = "┐(￣ヘ￣;)┌\nPlayer yang kamu masukan tidak terdaftar"
                em = discord.Embed(color = 0XFF8C00,
                                   description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)

            if LangCheck == "EN":
                msg = "┐(￣ヘ￣;)┌\nLooks like player that you entered is not registered"
                em = discord.Embed(color = 0XFF8C00,
                                   description = msg)
                em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
                await ctx.send(embed = em)
        except Exception as e:
            print (e)
            await ctx.send("**ERROR**\n```\n{}\n```".format(e))

    @commands.command(aliases = ["std"])
    async def osu(self, ctx, *, player = None):
        """**INDONESIA**
        Cek informasi player Osu!Standard.
        
        **ENGLISH**
        Check player information Osu!Standard."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.std_statistic(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.std_statistic(ctx, player)
        return

    @commands.command()
    async def taiko(self, ctx, *, player = None):
        """**INDONESIA**
        Cek informasi player Osu!Taiko.
        
        **ENGLISH**
        Check player information Osu!Taiko."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.taiko_statistic(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.taiko_statistic(ctx, player)
        return
        
    @commands.command()
    async def ctb(self, ctx, *, player = None):
        """**INDONESIA**
        Cek informasi player Osu!Catch.
        
        **ENGLISH**
        Check player information Osu!Catch."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.ctb_statistic(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.ctb_statistic(ctx, player)
        return
        
    @commands.command()
    async def mania(self, ctx, *, player = None):
        """**INDONESIA**
        Cek informasi player Osu!Mania.
        
        **ENGLISH**
        Check player information Osu!Mania."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.mania_statistic(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.mania_statistic(ctx, player)
        return
    

    @commands.command(aliases = ["rosu"])
    async def rstd(self, ctx, *, player = None):
        """**INDONESIA**
        Cek recent game Osu!Standard.
        
        **ENGLISH**
        Check recent game Osu!Standard."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.osu_standard_recent(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.osu_standard_recent(ctx, player)
        return


    @commands.command()
    async def rtaiko(self, ctx, *, player = None):
        """**INDONESIA**
        Cek recent game Osu!Taiko.
        
        **ENGLISH**
        Check recent game Osu!Taiko"""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.taiko_standard_recent(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.taiko_standard_recent(ctx, player)
        return


    @commands.command(aliases = ["rctb"])
    async def rcatch(self, ctx, *, player = None):
        """**INDONESIA**
        Cek recent game Osu!Catch.
        
        **ENGLISH**
        Check recent game Osu!Catch."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.ctb_standard_recent(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.ctb_standard_recent(ctx, player)
        return


    @commands.command()
    async def rmania(self, ctx, *, player = None):
        """**INDONESIA**
        Cek recent game Osu!Mania.
        
        **ENGLISH**
        Check recent game Osu!Mania."""
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == None:
            await self.language_not_set(ctx)

        if type(player) == str:
            playerName = player
            await self.mania_standard_recent(ctx, playerName)
            return
        
        player = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "OsuPlayer")

        if player == None:
            return await self.player_not_found(ctx)

        await self.mania_standard_recent(ctx, player)
        return


    async def player_not_found(self, ctx):
        LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
        if LangCheck == "ID":
            msg =  "> Kamu belum mengatur Osu!player dalam server ini.\n"
            msg += "> Silahkan ketik *`{}setosu [player]`*\n".format(ctx.prefix)
            msg += "> **Contoh**\n"
            msg += "> *`{}setosu kazereborn`*".format(ctx.prefix)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "Oops", 
                          icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Osu%21Logo_%282015%29.svg/1200px-Osu%21Logo_%282015%29.svg.png")
            em.set_footer(text = f"{ctx.author}",
                          icon_url = f"{ctx.author.avatar_url}")
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg =  "> You have not set your Osu!player in this server.\n"
            msg += "> Please type *`{}setosu [player]`*\n".format(ctx.prefix)
            msg += "> **Example**\n"
            msg += "> *`{}setosu kazereborn`*".format(ctx.prefix)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "Oops", 
                          icon_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Osu%21Logo_%282015%29.svg/1200px-Osu%21Logo_%282015%29.svg.png")
            em.set_footer(text = f"{ctx.author}",
                          icon_url = f"{ctx.author.avatar_url}")
            return await ctx.send(embed = em)
    
    async def std_statistic(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        # STATISTIC PLAYER
        r = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=0&u={}".format(player))
        data = r.text
        data = json.loads(data)
        a = data
        #BEST PERFORMANCE
        r2 = requests.get("https://osu.ppy.sh/api/get_user_best?k=526d85b33ad4b0912850229a00e17e91b612d653&limit=1&m=0&u={}".format(str(a[0]["username"])))
        data2 = r2.text
        data2 = json.loads(data2)
        b = data2
        # BEATMAPS
        r3 = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(str(b[0]["beatmap_id"])))
        data3 = r3.text
        data3 = json.loads(data3)
        c = data3
        # PEMBULATAN KABAWAH UNTUK LEVEL
        level = a[0]["level"]
        flevel = float(level)
        rlevel = int(flevel)
        # PEMBULATAN KEBAWAH UNTUK PERFORMANCE
        pp = a[0]["pp_raw"]
        fpp = float(pp)
        rpp = int(fpp)
        # PEMBULATAN KEBAWAH UNTUK AKURASI
        acc = a[0]["accuracy"]
        facc = float(acc)
        racc = int(facc)
        # PEMBULATAN UNTUK BEST PERFORMANCE
        bpp = b[0]["pp"]
        rbpp = float(bpp)
        rbpp = round(rbpp)
        # PENGAMBILAN 2 ANGKA DI BELAKANG KOMA UNTUK DIFFICULT BEATMAPS
        dbm = c[0]["difficultyrating"]
        rdbm = "{:.2f}".format(float(dbm))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        tds = b[0]["score"]
        ttds = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(tds))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK PLAYCOUNT
        playCount = a[0]["playcount"]
        playCount = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(playCount))
        # ICON FLAG
        country = a[0]["country"]
        countryId = country.lower()
        print (countryId)
        flagimg = "https://flagpedia.net/data/flags/w702/{}.webp".format(countryId)
        # EMBED BOT UNTUK STATISTIC PLAYER
        if LangCheck == "ID":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Akurasi       : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Bermain : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Standard profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)
        
        if LangCheck == "EN":
            msg =  "Player ID     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Accuracy      : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Play    : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Standard profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)
      except:
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ditemukan.".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

        if LangCheck == "EN":
            msg = "Player *`{}`* is not found.".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
        
    async def taiko_statistic(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        # STATISTIC PLAYER
        r = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=1&u={}".format(player))
        data = r.text
        data = json.loads(data)
        a = data
        #BEST PERFORMANCE
        r2 = requests.get("https://osu.ppy.sh/api/get_user_best?k=526d85b33ad4b0912850229a00e17e91b612d653&limit=1&m=1&u={}".format(str(a[0]["username"])))
        data2 = r2.text
        data2 = json.loads(data2)
        b = data2
        # BEATMAPS
        r3 = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(str(b[0]["beatmap_id"])))
        data3 = r3.text
        data3 = json.loads(data3)
        c = data3
        # PEMBULATAN KABAWAH UNTUK LEVEL
        level = a[0]["level"]
        flevel = float(level)
        rlevel = int(flevel)
        # PEMBULATAN KEBAWAH UNTUK PERFORMANCE
        pp = a[0]["pp_raw"]
        fpp = float(pp)
        rpp = int(fpp)
        # PEMBULATAN KEBAWAH UNTUK AKURASI
        acc = a[0]["accuracy"]
        facc = float(acc)
        racc = int(facc)
        # PEMBULATAN UNTUK BEST PERFORMANCE
        bpp = b[0]["pp"]
        rbpp = float(bpp)
        rbpp = round(rbpp)
        # PENGAMBILAN 2 ANGKA DI BELAKANG KOMA UNTUK DIFFICULT BEATMAPS
        dbm = c[0]["difficultyrating"]
        rdbm = "{:.2f}".format(float(dbm))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        tds = b[0]["score"]
        ttds = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(tds))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK PLAYCOUNT
        playCount = a[0]["playcount"]
        playCount = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(playCount))
        # ICON FLAG
        country = a[0]["country"]
        countryId = country.lower()
        print (countryId)
        flagimg = "https://flagpedia.net/data/flags/w702/{}.webp".format(countryId)
        # EMBED BOT UNTUK STATISTIC PLAYER
        if LangCheck == "ID":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Akurasi       : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Bermain : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Taiko profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&mode=1&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)
        
        if LangCheck == "EN":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Accuracy      : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Play    : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Taiko profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&mode=1&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)
      except:
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ditemukan".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
        if LangCheck == "EN":
            msg = "Player *`{}`* is not found".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)


    async def ctb_statistic(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        # STATISTIC PLAYER
        r = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=2&u={}".format(player))
        data = r.text
        data = json.loads(data)
        a = data
        #BEST PERFORMANCE
        r2 = requests.get("https://osu.ppy.sh/api/get_user_best?k=526d85b33ad4b0912850229a00e17e91b612d653&limit=1&m=2&u={}".format(str(a[0]["username"])))
        data2 = r2.text
        data2 = json.loads(data2)
        b = data2
        # BEATMAPS
        r3 = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(str(b[0]["beatmap_id"])))
        data3 = r3.text
        data3 = json.loads(data3)
        c = data3
        # PEMBULATAN KABAWAH UNTUK LEVEL
        level = a[0]["level"]
        flevel = float(level)
        rlevel = int(flevel)
        # PEMBULATAN KEBAWAH UNTUK PERFORMANCE
        pp = a[0]["pp_raw"]
        fpp = float(pp)
        rpp = int(fpp)
        # PEMBULATAN KEBAWAH UNTUK AKURASI
        acc = a[0]["accuracy"]
        facc = float(acc)
        racc = int(facc)
        # PEMBULATAN UNTUK BEST PERFORMANCE
        bpp = b[0]["pp"]
        rbpp = float(bpp)
        rbpp = round(rbpp)
        # PENGAMBILAN 2 ANGKA DI BELAKANG KOMA UNTUK DIFFICULT BEATMAPS
        dbm = c[0]["difficultyrating"]
        rdbm = "{:.2f}".format(float(dbm))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        tds = b[0]["score"]
        ttds = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(tds))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK PLAYCOUNT
        playCount = a[0]["playcount"]
        playCount = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(playCount))
        # ICON FLAG
        country = a[0]["country"]
        countryId = country.lower()
        print (countryId)
        flagimg = "https://flagpedia.net/data/flags/w702/{}.webp".format(countryId)
        # EMBED BOT UNTUK STATISTIC PLAYER
        if LangCheck == "ID":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Akurasi       : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Bermain : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Catch profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&mode=2&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)

        if LangCheck == "EN":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Accuracy      : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Play    : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Catch profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&mode=2&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)

      except:
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ditemukan".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg = "Player *`{}`* is not found".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
    async def mania_statistic(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        # STATISTIC PLAYER
        r = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=3&u={}".format(player))
        data = r.text
        data = json.loads(data)
        a = data
        #BEST PERFORMANCE
        r2 = requests.get("https://osu.ppy.sh/api/get_user_best?k=526d85b33ad4b0912850229a00e17e91b612d653&limit=1&m=3&u={}".format(str(a[0]["username"])))
        data2 = r2.text
        data2 = json.loads(data2)
        b = data2
        # BEATMAPS
        r3 = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(str(b[0]["beatmap_id"])))
        data3 = r3.text
        data3 = json.loads(data3)
        c = data3
        # PEMBULATAN KABAWAH UNTUK LEVEL
        level = a[0]["level"]
        flevel = float(level)
        rlevel = int(flevel)
        # PEMBULATAN KEBAWAH UNTUK PERFORMANCE
        pp = a[0]["pp_raw"]
        fpp = float(pp)
        rpp = int(fpp)
        # PEMBULATAN KEBAWAH UNTUK AKURASI
        acc = a[0]["accuracy"]
        facc = float(acc)
        racc = int(facc)
        # PEMBULATAN UNTUK BEST PERFORMANCE
        bpp = b[0]["pp"]
        rbpp = float(bpp)
        rbpp = round(rbpp)
        # PENGAMBILAN 2 ANGKA DI BELAKANG KOMA UNTUK DIFFICULT BEATMAPS
        dbm = c[0]["difficultyrating"]
        rdbm = "{:.2f}".format(float(dbm))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        tds = b[0]["score"]
        ttds = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(tds))
        # PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK PLAYCOUNT
        playCount = a[0]["playcount"]
        playCount = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(playCount))
        # ICON FLAG
        country = a[0]["country"]
        countryId = country.lower()
        print (countryId)
        flagimg = "https://flagpedia.net/data/flags/w702/{}.webp".format(countryId)
        # EMBED BOT UNTUK STATISTIC PLAYER
        if LangCheck == "ID":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Akurasi       : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Bermain : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Mania profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&mode=3&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)

        if LangCheck == "EN":
            msg =  "ID Player     : {}\n".format(str(a[0]["user_id"]))
            msg += "Level         : {}\n".format(str(rlevel))
            msg += "Performance   : {}pp\n".format(str(rpp))
            msg += "Accuracy      : {}%\n".format(str(racc))
            msg += "Global Rank   : #{}\n".format(str(a[0]["pp_rank"]))
            msg += "Local Rank    : {}#{}\n".format(country, str(a[0]["pp_country_rank"]))
            msg += "Total Play    : {}".format(playCount)
            em = discord.Embed(color = 0XFF8C00, description = "```\n{}\n```".format(msg))
            em.set_author(name = "Osu!Mania profile {}".format(str(a[0]["username"])),
                          icon_url = "{}".format(flagimg))
            TotalRank =  "<:ARank:788996704301088779> {}  ".format(a[0]["count_rank_a"])
            TotalRank += "<:SRank:788996986359251006> {}  ".format(a[0]["count_rank_s"])
            TotalRank += "<:SHRank:788997286477824022> {}  ".format(a[0]["count_rank_sh"])
            TotalRank += "<:SSRank:788997396470300712> {}  ".format(a[0]["count_rank_ss"])
            TotalRank += "<:SSHRank:788997506684026921> {}".format(a[0]["count_rank_ssh"])
            em.add_field(name = "Total Rank", value = TotalRank)
            em.add_field(name = "Homepage Link", value = "https://osu.ppy.sh/users/{}".format(str(a[0]["user_id"])), inline = False)
            em.set_footer(text = f"{ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url = "http://lemmmy.pw/osusig/sig.php?colour=hexee8833&uname={}&mode=3&removeavmargin&flagshadow&flagstroke&darkheader&darktriangles&opaqueavatar&rankedscore&onlineindicator=undefined&xpbar&xpbarhex".format(str(a[0]["user_id"])))
            msg = await ctx.send(embed = em)

      except:
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ditemukan".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg = "Player *`{}`* is not found".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        
    async def osu_standard_recent(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        #Get recent
        OsuRecent = requests.get("https://osu.ppy.sh/api/get_user_recent?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}&m=0&limit=1".format(player))
        data = OsuRecent.text
        dataRecent = json.loads(data)
        getRecent = dataRecent
        #Get player
        OsuPlayer = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=0&u={}".format(player))
        data = OsuPlayer.text
        dataPlayer = json.loads(data)
        getPlayer = dataPlayer
        #Get beatmap
        OsuBeatmap = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(getRecent[0]["beatmap_id"]))
        data = OsuBeatmap.text
        dataBeatmap = json.loads(data)
        getBeatmap = dataBeatmap
        #PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        checkScore = getRecent[0]["score"]
        score = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(checkScore))
        #Penambahan titik setiap 3 digit untuk combo
        checkCombo = getRecent[0]["maxcombo"]
        combo = re.sub(r"(?<!^)(?=(/d{3})+$)", r".", "{}".format(checkCombo))
        #Pengambilan 2 angka dibelakang koma untuk difficult beatmap
        checkDifficult = getBeatmap[0]["difficultyrating"]
        difficult = "{:.2f}".format(float(checkDifficult))
        #Perhitungan Akurasi
        n300   = (int(getRecent[0]["count300"]))
        n100   = (int(getRecent[0]["count100"]))
        n50    = (int(getRecent[0]["count50"]))
        nMiss  = (int(getRecent[0]["countmiss"]))
        n300sub= n300 / 1
        n100sub= n100 / 3
        n50sub = n50  / 6
        nTotal = n300sub + n100sub + n50sub
        cTotal = nMiss + n50 + n100 + n300
        subTotal = nTotal / cTotal
        subTotal = subTotal * 100
        totalAcc = "{:.2f}".format(float(subTotal))
        #GET MODS
        getMods = (getRecent[0]["enabled_mods"])
        mods = num_to_mod(getMods)
        modsEmoji = num_to_mod_emoticon(getMods)
        modsPP = ''.join(mods)
        modsEmoji = ''.join(modsEmoji)
        #Get PP
        # getPerformance = subprocess.Popen(["python3.8", "console_calc.py", "-l", "https://osu.ppy.sh/b/{}".format(getBeatmap[0]["beatmap_id"]),"-c100","{}".format(n100),"-c50","{}".format(n50),"-m","{}".format(nMiss),"-c","{}".format(getBeatmap[0]["max_combo"]), "-acc", "{}".format(totalAcc), "-mods", "{}".format(modsPP)], stdout = subprocess.PIPE).communicate()[0]
        # getPerformance = json.loads(json.dumps(eval(getPerformance)))
        # performance = getPerformance["pp"]
        # print (getPerformance)
        #Lets Build everything
        perfect = getRecent[0]["perfect"]
        getRank = getRecent[0]["rank"]
        
        if getRank == "XH":
            rankEmoji = "<:SSHRank:788997506684026921>"
        elif getRank == "X":
            rankEmoji = "<:SSRank:788997396470300712>"
        elif getRank == "SH":
            rankEmoji = "<:SHRank:788997286477824022>"
        elif getRank == "S":
            rankEmoji = "<:SRank:788996986359251006>"
        elif getRank == "A":
            rankEmoji = "<:ARank:788996704301088779>"
        elif getRank == "B":
            rankEmoji = "<:BRank:789798037915435018>"
        elif getRank == "C":
            rankEmoji = "<:CRank:789798155600396299>"
        elif getRank == "D":
            rankEmoji = "<:DRank:789798233383108618>"
        elif getRank == "F":
            rankEmoji = "<:FRank:790106142722228256>"
            
        if perfect == "1":
            msg =  "{}\n".format(modsEmoji)
            msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
            msg += "ACC: {}%\n".format(totalAcc)
            msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
            msg += "<:countKatu:789815141168447538> {}  <:count50:789815600553394196> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["count50"], getRecent[0]["countmiss"])
            msg += "{}".format(getRecent[0]["date"])
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                          url = "https://osu.ppy.sh/b/{}".format(getBeatmap[0]["beatmap_id"]),
                          icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
            #em.set_thumbnail(url = "https://b.ppy.sh/thumb/{}l.jpg".format(getBeatmap[0]["beatmapset_id"]))
            em.set_image(url = "https://cdn.discordapp.com/attachments/744831859543769199/790054724014964786/37838.png")
            em.set_footer(text = "CONGRATULATION YOU GOT FULL COMBO\n{}".format(ctx.author), 
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(content = "**{} Osu!Standard Recent Play**".format(getPlayer[0]["username"]),embed = em)
        
        msg = "{}\n".format(modsEmoji)
        msg +=  "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
        msg += "ACC: {}%\n".format(totalAcc)
        msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
        msg += "<:countKatu:789815141168447538> {}  <:count50:789815600553394196> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["count50"], getRecent[0]["countmiss"])
        msg += "{}".format(getRecent[0]["date"])
        em = discord.Embed(color = 0XFF8C00,
                           description = msg)
        em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                      url = "https://osu.ppy.sh/b/{}".format(getBeatmap[0]["beatmap_id"]),
                      icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
        em.set_thumbnail(url = "https://b.ppy.sh/thumb/{}l.jpg".format(getBeatmap[0]["beatmapset_id"]))
        em.set_footer(text = "PRACTICE MAKE YOU PERFECT\n{}".format(ctx.author),
                      icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(content = "**{} Osu!Standard Recent Play**".format(getPlayer[0]["username"]), embed = em)
      except Exception as e:
        print (e)
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ada recent game yang terekam server Osu!".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg = "There is no recent game for player *`{}`!*".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

    async def taiko_standard_recent(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        #Get recent
        OsuRecent = requests.get("https://osu.ppy.sh/api/get_user_recent?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}&m=1&limit=1".format(player))
        data = OsuRecent.text
        dataRecent = json.loads(data)
        getRecent = dataRecent
        #Get player
        OsuPlayer = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=1&u={}".format(player))
        data = OsuPlayer.text
        dataPlayer = json.loads(data)
        getPlayer = dataPlayer
        #Get beatmap
        OsuBeatmap = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(getRecent[0]["beatmap_id"]))
        data = OsuBeatmap.text
        dataBeatmap = json.loads(data)
        getBeatmap = dataBeatmap
        #PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        checkScore = getRecent[0]["score"]
        score = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(checkScore))
        #Penambahan titik setiap 3 digit untuk combo
        checkCombo = getRecent[0]["maxcombo"]
        combo = re.sub(r"(?<!^)(?=(/d{3})+$)", r".", "{}".format(checkCombo))
        #Pengambilan 2 angka dibelakang koma untuk difficult beatmap
        checkDifficult = getBeatmap[0]["difficultyrating"]
        difficult = "{:.2f}".format(float(checkDifficult))
        print (difficult)
        #Perhitungan Akurasi Taiko
        n300   = (int(getRecent[0]["count300"]))
        n100   = (int(getRecent[0]["count100"]))
        n50    = (int(getRecent[0]["count50"]))
        nMiss  = (int(getRecent[0]["countmiss"]))
        n100sub = n100 * 0.5
        nTotal = n100sub + n300
        cTotal = nMiss + n100 + n300
        subTotal = nTotal / cTotal
        subTotal = subTotal * 100
        totalAcc = "{:.2f}".format(float(subTotal))
        #Get Mods
        getMods = (getRecent[0]["enabled_mods"])
        mods = num_to_mod(getMods)
        modsEmoji = num_to_mod_emoticon(getMods)
        modsPP = ''.join(mods)
        modsEmoji = ''.join(modsEmoji)
        #Lets Build everything
        perfect = getRecent[0]["perfect"]
        getRank = getRecent[0]["rank"]
        
        if getRank == "XH":
            rankEmoji = "<:SSHRank:788997506684026921>"
        elif getRank == "X":
            rankEmoji = "<:SSRank:788997396470300712>"
        elif getRank == "SH":
            rankEmoji = "<:SHRank:788997286477824022>"
        elif getRank == "S":
            rankEmoji = "<:SRank:788996986359251006>"
        elif getRank == "A":
            rankEmoji = "<:ARank:788996704301088779>"
        elif getRank == "B":
            rankEmoji = "<:BRank:789798037915435018>"
        elif getRank == "C":
            rankEmoji = "<:CRank:789798155600396299>"
        elif getRank == "D":
            rankEmoji = "<:DRank:789798233383108618>"
        elif getRank == "F":
            rankEmoji = "<:FRank:790106142722228256>"
            
        if perfect == "1":
            msg = "{}\n".format(modsEmoji)
            msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
            msg += "ACC : {}%\n".format(totalAcc)
            msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
            msg += "<:countKatu:789815141168447538> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["countmiss"])
            msg += "{}".format(getRecent[0]["date"])
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                          url = "https://osu.ppy.sh/beatmapsets/{}".format(getBeatmap[0]["beatmapset_id"]),
                          icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
            em.set_image(url = "https://cdn.discordapp.com/attachments/744831859543769199/789840607874383902/ranking-perfect.png")
            em.set_footer(text = "CONGRATULATION YOU GOT FULL COMBO\n{}".format(ctx.author), 
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(content = "**{} Osu!Taiko Recent Play**".format(getPlayer[0]["username"]),embed = em)
        
        mag = "{}\n".format(modsEmoji)
        msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
        msg += "ACC : {}%\n".format(totalAcc)
        msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
        msg += "<:countKatu:789815141168447538> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["countmiss"])
        msg += "{}".format(getRecent[0]["date"])
        em = discord.Embed(color = 0XFF8C00,
                           description = msg)
        em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                      url = "https://osu.ppy.sh/beatmapsets/{}".format(getBeatmap[0]["beatmapset_id"]),
                      icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
        em.set_thumbnail(url = "https://b.ppy.sh/thumb/{}l.jpg".format(getBeatmap[0]["beatmapset_id"]))
        em.set_footer(text = "PRACTICE MAKE YOU PERFECT\n{}".format(ctx.author),
                      icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(content = "**{} Osu!Taiko Recent Play**".format(getPlayer[0]["username"]), embed = em)
      except Exception as e:
        print (e)
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ada recent game yang terekam server Osu!".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg = "There is no recent game for player *`{}`!*".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

    async def ctb_standard_recent(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        #Get recent
        OsuRecent = requests.get("https://osu.ppy.sh/api/get_user_recent?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}&m=2&limit=1".format(player))
        data = OsuRecent.text
        dataRecent = json.loads(data)
        getRecent = dataRecent
        #Get player
        OsuPlayer = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=2&u={}".format(player))
        data = OsuPlayer.text
        dataPlayer = json.loads(data)
        getPlayer = dataPlayer
        #Get beatmap
        OsuBeatmap = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(getRecent[0]["beatmap_id"]))
        data = OsuBeatmap.text
        dataBeatmap = json.loads(data)
        getBeatmap = dataBeatmap
        print(getBeatmap)
        #PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        checkScore = getRecent[0]["score"]
        score = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(checkScore))
        #Penambahan titik setiap 3 digit untuk combo
        checkCombo = getRecent[0]["maxcombo"]
        combo = re.sub(r"(?<!^)(?=(/d{3})+$)", r".", "{}".format(checkCombo))
        #Pengambilan 2 angka dibelakang koma untuk difficult beatmap
        checkDifficult = getBeatmap[0]["difficultyrating"]
        difficult = "{:.2f}".format(float(checkDifficult))
        #Rumus perhitungan akurasi Catch
        nDroplets = (int(getRecent[0]["count50"]))
        nDropletMiss = (int(getRecent[0]["countkatu"]))
        nDrops = (int(getRecent[0]["count100"]))
        nFruits = (int(getRecent[0]["count300"]))
        nMiss = (int(getRecent[0]["countmiss"]))
        nTotal = nDroplets + nDrops + nFruits
        cTotal = nMiss + nDropletMiss + nDroplets + nDrops + nFruits
        subTotal = nTotal / cTotal
        subTotal = subTotal * 100
        totalAcc = "{:.2f}".format(float(subTotal))
        print(totalAcc)
        #Get mods
        getMods = (getRecent[0]["enabled_mods"])
        mods = num_to_mod(getMods)
        modsEmoji = num_to_mod_emoticon(getMods)
        modsPP = ''.join(mods)
        modsEmoji = ''.join(modsEmoji)
        #Lets build everything
        perfect = getRecent[0]["perfect"]
        getRank = getRecent[0]["rank"]
        
        if getRank == "XH":
            rankEmoji = "<:SSHRank:788997506684026921>"
        elif getRank == "X":
            rankEmoji = "<:SSRank:788997396470300712>"
        elif getRank == "SH":
            rankEmoji = "<:SHRank:788997286477824022>"
        elif getRank == "S":
            rankEmoji = "<:SRank:788996986359251006>"
        elif getRank == "A":
            rankEmoji = "<:ARank:788996704301088779>"
        elif getRank == "B":
            rankEmoji = "<:BRank:789798037915435018>"
        elif getRank == "C":
            rankEmoji = "<:CRank:789798155600396299>"
        elif getRank == "D":
            rankEmoji = "<:DRank:789798233383108618>"
        elif getRank == "F":
            rankEmoji = "<:FRank:790106142722228256>"
            
        if perfect == "1":
            msg =  "{}\n".format(modsEmoji)
            msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
            msg += "ACC : {}%\n".format(totalAcc)
            msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
            msg += "<:countKatu:789815141168447538> {}  <:count50:789815600553394196> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["count50"], getRecent[0]["countmiss"])
            msg += "{}".format(getRecent[0]["date"])
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                          url = "https://osu.ppy.sh/beatmapsets/{}".format(getBeatmap[0]["beatmapset_id"]),
                          icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
            #em.set_thumbnail(url = "https://b.ppy.sh/thumb/{}l.jpg".format(getBeatmap[0]["beatmapset_id"]))
            em.set_image(url = "https://cdn.discordapp.com/attachments/744831859543769199/790054724014964786/37838.png")
            em.set_footer(text = "CONGRATULATION YOU GOT FULL COMBO\n{}".format(ctx.author), 
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(content = "**{} Osu!Catch Recent Play**".format(getPlayer[0]["username"]),embed = em)
        
        msg =  "{}\n".format(modsEmoji)
        msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
        msg += "ACC : {}%\n".format(totalAcc)
        msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
        msg += "<:countKatu:789815141168447538> {}  <:count50:789815600553394196> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["count50"], getRecent[0]["countmiss"])
        msg += "{}".format(getRecent[0]["date"])
        em = discord.Embed(color = 0XFF8C00,
                           description = msg)
        em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                      url = "https://osu.ppy.sh/beatmapsets/{}".format(getBeatmap[0]["beatmapset_id"]),
                      icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
        em.set_thumbnail(url = "https://b.ppy.sh/thumb/{}l.jpg".format(getBeatmap[0]["beatmapset_id"]))
        em.set_footer(text = "PRACTICE MAKE YOU PERFECT\n{}".format(ctx.author),
                      icon_url = "{}".format(ctx.author.avatar_url))
        return await ctx.send(content = "**{} Osu!Catch Recent Play**".format(getPlayer[0]["username"]), embed = em)
      except Exception as e:
        print (e)
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ada recent game yang terekam server Osu!".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg = "There is no recent game for player *`{}`!*".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)


    async def mania_standard_recent(self, ctx, player):
      LangCheck = self.settings.getUserStat(ctx.message.author, ctx.message.guild, "Language")
      try:
        #Get recent
        OsuRecent = requests.get("https://osu.ppy.sh/api/get_user_recent?k=526d85b33ad4b0912850229a00e17e91b612d653&u={}&m=3&limit=1".format(player))
        data = OsuRecent.text
        dataRecent = json.loads(data)
        getRecent = dataRecent
        #Get player
        OsuPlayer = requests.get("https://osu.ppy.sh/api/get_user?k=526d85b33ad4b0912850229a00e17e91b612d653&m=3&u={}".format(player))
        data = OsuPlayer.text
        dataPlayer = json.loads(data)
        getPlayer = dataPlayer
        #Get beatmap
        OsuBeatmap = requests.get("https://osu.ppy.sh/api/get_beatmaps?k=526d85b33ad4b0912850229a00e17e91b612d653&b={}".format(getRecent[0]["beatmap_id"]))
        data = OsuBeatmap.text
        dataBeatmap = json.loads(data)
        getBeatmap = dataBeatmap
        #PENAMBAHAN TITIK SETIAP 3 DIGIT UNTUK SCORE
        checkScore = getRecent[0]["score"]
        score = re.sub(r"(?<!^)(?=(\d{3})+$)", r".", "{}".format(checkScore))
        #Penambahan titik setiap 3 digit untuk combo
        checkCombo = getRecent[0]["maxcombo"]
        combo = re.sub(r"(?<!^)(?=(/d{3})+$)", r".", "{}".format(checkCombo))
        #Pengambilan 2 angka dibelakang koma untuk difficult beatmap
        checkDifficult = getBeatmap[0]["difficultyrating"]
        difficult = "{:.2f}".format(float(checkDifficult))
        #Perhitungan rumus akurasi mania
        nMax    = (int(getRecent[0]["countgeki"]))
        n300    = (int(getRecent[0]["count300"]))
        n200    = (int(getRecent[0]["countkatu"]))
        n100    = (int(getRecent[0]["count100"]))
        n50     = (int(getRecent[0]["count50"]))
        nMiss   = (int(getRecent[0]["countmiss"]))
        n50sub  = n50  * 50
        n100sub = n100 * 100
        n200sub = n200 * 200
        n300sub = n300 * 300
        nMaxsub = nMax * 300
        nTotal  = n50sub + n100sub + n200sub + n300sub + nMaxsub
        cTotal  = nMax + n300 + n200 + n100 + n50 + nMiss
        cTotal  = cTotal * 300
        subTotal = nTotal / cTotal
        subTotal = subTotal * 100
        totalAcc = "{:.2f}".format(float(subTotal))
        #Get mods
        getMods = (getRecent[0]["enabled_mods"])
        mods = num_to_mod(getMods)
        modsEmoji = num_to_mod_emoticon(getMods)
        modsPP = ''.join(mods)
        modsEmoji = ''.join(modsEmoji)
        #Lets Build everything
        perfect = getRecent[0]["perfect"]
        getRank = getRecent[0]["rank"]
        
        if getRank == "XH":
            rankEmoji = "<:SSHRank:788997506684026921>"
        elif getRank == "X":
            rankEmoji = "<:SSRank:788997396470300712>"
        elif getRank == "SH":
            rankEmoji = "<:SHRank:788997286477824022>"
        elif getRank == "S":
            rankEmoji = "<:SRank:788996986359251006>"
        elif getRank == "A":
            rankEmoji = "<:ARank:788996704301088779>"
        elif getRank == "B":
            rankEmoji = "<:BRank:789798037915435018>"
        elif getRank == "C":
            rankEmoji = "<:CRank:789798155600396299>"
        elif getRank == "D":
            rankEmoji = "<:DRank:789798233383108618>"
        elif getRank == "F":
            rankEmoji = "<:FRank:790106142722228256>"
        
        if perfect == "1":
            msg =  "{}\n".format(modsEmoji)
            msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
            msg += "ACC : {}%\n".format(totalAcc)
            msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
            msg += "<:countKatu:789815141168447538> {}  <:count50:789815600553394196> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["count50"], getRecent[0]["countmiss"])
            msg += ""
            msg += "{}".format(getRecent[0]["date"])
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                          url = "https://osu.ppy.sh/beatmapsets/{}".format(getBeatmap[0]["beatmapset_id"]),
                          icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
            em.set_image(url = "https://cdn.discordapp.com/attachments/744831859543769199/789840607874383902/ranking-perfect.png")
            em.set_footer(text = "CONGRATULATION YOU GOT FULL COMBO\n{}".format(ctx.author), 
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(content = "**{} Osu!Mania Recent Play**".format(getPlayer[0]["username"]),embed = em)
        
        if perfect == "0":
            msg =  "{}\n".format(modsEmoji)
            msg += "{} {} ({}/{})\n".format(rankEmoji, score, combo, getBeatmap[0]["max_combo"])
            msg += "ACC : {}%\n".format(totalAcc)
            msg += "<:count300:789814804914372633> {}  <:countGeki:789814942785077258> {}  <:count100:789815074507849738> {}  ".format(getRecent[0]["count300"], getRecent[0]["countgeki"], getRecent[0]["count100"])
            msg += "<:countKatu:789815141168447538> {}  <:count50:789815600553394196> {}  <:countMiss:789815688834842635> {}\n".format(getRecent[0]["countkatu"], getRecent[0]["count50"], getRecent[0]["countmiss"])
            msg += "{}".format(getRecent[0]["date"])
            em = discord.Embed(color = 0XFF8C00,
                           description = msg)
            em.set_author(name = "{} [{}]\n[{}☆]".format(getBeatmap[0]["title"], getBeatmap[0]["version"], difficult),
                          url = "https://osu.ppy.sh/beatmapsets/{}".format(getBeatmap[0]["beatmapset_id"]),
                          icon_url = "http://s.ppy.sh/a/{}".format(getPlayer[0]["user_id"]))
            em.set_thumbnail(url = "https://b.ppy.sh/thumb/{}l.jpg".format(getBeatmap[0]["beatmapset_id"]))
            em.set_footer(text = "PRACTICE MAKE YOU PERFECT\n{}".format(ctx.author),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(content = "**{} Osu!Mania Recent Play**".format(getPlayer[0]["username"]), embed = em)
      except Exception as e:
        print (e)
        if LangCheck == "ID":
            msg = "Player *`{}`* tidak ada recent game yang terekam server Osu!".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        if LangCheck == "EN":
            msg = "There is no recent game for player *`{}`!*".format(player)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)

    async def language_not_set(self, ctx):
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

def num_to_mod(number):
    number = int(number)
    mod_list = []

    if number & 1<<0:   mod_list.append('NF')
    if number & 1<<1:   mod_list.append('EZ')
    if number & 1<<3:   mod_list.append('HD')
    if number & 1<<4:   mod_list.append('HR')
    if number & 1<<5:   mod_list.append('SD')
    if number & 1<<9:   mod_list.append('NC')
    elif number & 1<<6: mod_list.append('DT')
    if number & 1<<7:   mod_list.append('RX')
    if number & 1<<8:   mod_list.append('HT')
    if number & 1<<10:  mod_list.append('FL')
    if number & 1<<12:  mod_list.append('SO')
    if number & 1<<14:  mod_list.append('PF')
    if number & 1<<15:  mod_list.append('4 KEY')
    if number & 1<<16:  mod_list.append('5 KEY')
    if number & 1<<17:  mod_list.append('6 KEY')
    if number & 1<<18:  mod_list.append('7 KEY')
    if number & 1<<19:  mod_list.append('8 KEY')
    if number & 1<<20:  mod_list.append('FI')
    if number & 1<<24:  mod_list.append('9 KEY')
    if number & 1<<25:  mod_list.append('10 KEY')
    if number & 1<<26:  mod_list.append('1 KEY')
    if number & 1<<27:  mod_list.append('3 KEY')
    if number & 1<<28:  mod_list.append('2 KEY')

    return mod_list

def num_to_mod_emoticon(number):
    number = int(number)
    mod_list = []

    if number & 1<<0:   mod_list.append('<:NoFail:790989105487675423>')
    if number & 1<<1:   mod_list.append('<:Easy:790989105642078288>')
    if number & 1<<3:   mod_list.append('<:Hidden:790989105856774184>')
    if number & 1<<4:   mod_list.append('<:HardRock:790989105684676609>')
    if number & 1<<5:   mod_list.append('<:SuddenDeath:790989105680351274>')
    if number & 1<<9:   mod_list.append('<:Nightcore:790989105844453436>')
    elif number & 1<<6: mod_list.append('<:DoubleTime:790989105659510814>')
    if number & 1<<7:   mod_list.append('<:Relax:790989105932402759>')
    if number & 1<<8:   mod_list.append('<:HalfTime:790989105608654848>')
    if number & 1<<10:  mod_list.append('<:Flashlight:790989105609572392>')
    if number & 1<<12:  mod_list.append('<:SpunOut:790989105810243655>')
    if number & 1<<14:  mod_list.append('<:Perfect:790989106334138408>')
    if number & 1<<15:  mod_list.append('<:4K:790992355649650708>')
    if number & 1<<16:  mod_list.append('<:5K:790992355733012501>')
    if number & 1<<17:  mod_list.append('<:6K:790992355569827840>')
    if number & 1<<18:  mod_list.append('<:7K:790992355422896158>')
    if number & 1<<19:  mod_list.append('<:8K:790992355582148618>')
    if number & 1<<20:  mod_list.append('<:FadeIn:790991502209318922>')
    if number & 1<<24:  mod_list.append('<:9K:790992355514646599>')
    if number & 1<<25:  mod_list.append('<:10K:790993374689493021>')
    if number & 1<<26:  mod_list.append('<:1K:790992520640856064>')
    if number & 1<<27:  mod_list.append('<:3K:790992355296804924>')
    if number & 1<<28:  mod_list.append('<:2K:790992354945269833>')

    return mod_list


