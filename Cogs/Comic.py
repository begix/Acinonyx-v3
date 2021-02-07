import asyncio
import discord
import random
import time
import datetime as dt
from   discord.ext import commands
from   Cogs import Settings
from   Cogs import GetImage
from   Cogs import ComicHelper
from   Cogs import DL
from   Cogs import Message

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Comic(bot, settings))

# This module will probably get comics... *finges crossed*

class Comic(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
    
    def getRandDateBetween(self, first, last):
        # Takes two date strings "MM-DD-YYYY" and
        # returns a dict of day, month, and year values
        # from a random date between them
        fDate = first.split("-")
        fJDate = ComicHelper.date_to_jd(int(fDate[2]), int(fDate[0]), int(fDate[1]))
        lDate = last.split("-")
        lJDate = ComicHelper.date_to_jd(int(lDate[2]), int(lDate[0]), int(lDate[1]))
        
        # Get random Julian Date
        randJDate = random.uniform(fJDate, lJDate)
        
        # Convert to gregorian
        gDate = ComicHelper.jd_to_date(randJDate)
        yea   = int(gDate[0])
        mon   = int(gDate[1])
        day   = int(gDate[2])
        
        # Make sure all months/days are double digits
        if (int(mon) < 10):
            mon = "0"+str(mon)
        if (int(day) < 10):
            day = "0"+str(day)
        
        # Build our dict and return it
        newDate = { "Year" : str(yea), "Month" : str(mon), "Day" : str(day)}
        return newDate
        
    
    def dateDict(self, date):
        # Takes a MM-DD-YYYY string or array
        # and converts it to a dict
        if type(date) == str:
            # Split by "-"
            date = date.split("-")
        
        yea   = int(date[2])
        mon   = int(date[0])
        day   = int(date[1])
        # Make sure all months/days are double digits
        if (int(mon) < 10):
            mon = "0"+str(mon)
        if (int(day) < 10):
            day = "0"+str(day)
        # Build our dict and return it
        newDate = { "Year" : str(yea), "Month" : str(mon), "Day" : str(day)}
        return newDate
        
        
        
    def isDateBetween(self, check, first, last):
        # Takes three date strings "MM-DD-YYY" and
        # returns whether the first is between the next two
        fDate = first.split("-")
        fJDate = ComicHelper.date_to_jd(int(fDate[2]), int(fDate[0]), int(fDate[1]))
        lDate = last.split("-")
        lJDate = ComicHelper.date_to_jd(int(lDate[2]), int(lDate[0]), int(lDate[1]))
        cDate = check.split("-")
        cJDate = ComicHelper.date_to_jd(int(cDate[2]), int(cDate[0]), int(cDate[1]))
        
        if cJDate <= lJDate and cJDate >= fJDate:
            return True
        else:
            return False
            
    def dateIsValid(self, date : str = None):
        # Checks if a passed date is a valid MM-DD-YYYY string
        if not date:
            # Auto to today's date
            date = dt.datetime.today().strftime("%m-%d-%Y")
        try:
            startDate = date.split("-")
        except ValueError:
            # Doesn't split by -?  Not valid
            return False
            
        if len(startDate) < 3:
            # Not enough values
            return False
            
        for d in startDate:
            try:
                int(d)
            except ValueError:
                return False
        
        return True
        
    def canDisplay(self, server):
        # Check if we can display images
        lastTime = int(self.settings.getServerStat(server, "LastPicture"))
        threshold = int(self.settings.getServerStat(server, "PictureThreshold"))
        if not GetImage.canDisplay( lastTime, threshold ):
            # await channel.send('Too many images at once - please wait a few seconds.')
            return False
        
        # If we made it here - set the LastPicture method
        self.settings.setServerStat(server, "LastPicture", int(time.time()))
        return True

    
    def buildDilbertURL(self, date):
        return "http://dilbert.com/strip/" + str(date['Year']) + "-" + str(date['Month']) + "-" + str(date['Day'])
        
      # ####### #
     # Dilbert #
    # ####### #
    @commands.command(pass_context=True)
    async def randilbert(self, ctx):
        """Mencari komik Dilbert secara random."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if not self.canDisplay(server):
            return
        
        # Get some preliminary values
        todayDate = dt.datetime.today().strftime("%m-%d-%Y")
        # Can't be before this date.
        firstDate = "04-16-1989"

        # Start a loop to find a comic
        gotComic = False
        tries = 0
        while not gotComic:
    
            if tries >= 10:
                break
        
            # Try to get a valid comic
            date      = self.getRandDateBetween(firstDate, todayDate)
            url       = self.buildDilbertURL(date)
            imageHTML = await ComicHelper.getImageHTML(url)
            
            if imageHTML:
                # Got it!
                gotComic = True
                
            # Increment try counter
            tries += 1  
        
        if tries >= 10:
            msg = 'Gagal mendapatkan link, coba lagi nanti.'
            await channel.send(msg)
            return
        
        # Got a comic link
        imageURL  = ComicHelper.getImageURL(imageHTML)
        imageDisplayName = ComicHelper.getImageTitle(imageHTML)
        if imageDisplayName.lower().startswith("dilbert comic for "):
            d = imageDisplayName.split(" ")[-1].split("-")
            imageDisplayName = "Dilbert Comic tanggal {}-{}-{}".format(d[1], d[2], d[0])
        
        # Download Image
        if not imageURL.lower().startswith("http"):
            imageURL = "https:"+imageURL
        await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL, imageDisplayName)
        
        
    @commands.command(pass_context=True)
    async def dilbert(self, ctx, *, date : str = None):
        """Mencari komik Dilbert dari tanggal yang di tentukan (MM-DD-YYYY)."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if date is None:
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://dilbert.com\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}dilbert [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randilbert` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        if not self.canDisplay(server):
            return
            
        if not date:
            # Auto to today's date
            date = dt.datetime.today().strftime("%m-%d-%Y")

        if not self.dateIsValid(date):
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://dilbert.com\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}dilbert [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randilbert` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        todayDate = dt.datetime.today().strftime("%m-%d-%Y")
        firstDate = "04-16-1989"
        
        if not self.isDateBetween(date, firstDate, todayDate):
            em = discord.Embed(color = 0XFF8C00, description = "> Tanggal tidak ditemukan\n"
                                                               "> Kamu harus mencari tanggal dari `{}`\n"
                                                               "> sampai tanggal `{}`\n> \n"
                                                               "> Kalau kamu gak mau ribet gunakan `{}randilbert` untuk mencari komik secara random"
                                                               .format(firstDate,
                                                                       todayDate,
                                                                       ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        url       = self.buildDilbertURL(self.dateDict(date))
        imageHTML = await ComicHelper.getImageHTML(url)
        
        if not imageHTML:
            em = discord.Embed(color = 0XFF8C00, description = "> Komik tidak ditemukan untuk tanggal {}\n> \n"
                                                               "> Kamu harus mencari tanggal dari `{}`\n"
                                                               "> sampai tanggal `{}`\n> \n"
                                                               "> Kalau kamu gak mau ribet gunakan `{}randilbert` untuk mencari komik secara random"
                                                               .format(date,
                                                                       firstDate,
                                                                       todayDate,
                                                                       ctx.prefix))
            em.set_author(name = "Komik tidak ditemukan", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
            
        imageURL  = ComicHelper.getImageURL(imageHTML)
        imageDisplayName = ComicHelper.getImageTitle(imageHTML)
        if imageDisplayName.lower().startswith("dilbert comic for "):
            d = imageDisplayName.split(" ")[-1].split("-")
            imageDisplayName = "Dilbert Comic tanggal {}-{}-{}".format(d[1], d[2], d[0])
        
        # Download Image
        if not imageURL.lower().startswith("http"):
            imageURL = "https:"+imageURL
        await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL, imageDisplayName)
        
      # #### #
     # XKCD #
    # #### #
    @commands.command(pass_context=True)
    async def randxkcd(self, ctx):
        """Menampilkan komik random dari XKCD."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if not self.canDisplay(server):
            return
        
        # Must be a comic number
        archiveURL = "http://xkcd.com/archive/"
        archiveHTML = await ComicHelper.getImageHTML(archiveURL)
        newest = int(ComicHelper.getNewestXKCD(archiveHTML))
        
        # Start a loop to find a comic
        gotComic = False
        tries = 0
        while not gotComic:
    
            if tries >= 10:
                break
        
            # Build our url
            date = random.randint(1, newest)
            comicURL = "http://xkcd.com/" + str(date) + "/"

            # now we get the actual comic info
            imageHTML = await ComicHelper.getImageHTML(comicURL)
        
            if imageHTML:
                gotComic = True
            
            tries += 1
            
        if tries >= 10:
            msg = 'Gagal mendapatkan gambar, coba lagi nanti.'
            await channel.send(msg)
            return
        
        # Got a comic link
        imageURL = ComicHelper.getXKCDImageURL(imageHTML)
        imageDisplayName = ComicHelper.getXKCDImageTitle(imageHTML)
        imageText = ComicHelper.getXKCDImageText(imageHTML)
        title = '{} *({})*'.format(imageDisplayName, date)

        # Download Image
        await Message.Embed(title=title, image=imageURL, url=imageURL, description=imageText, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL, title)


    @commands.command(pass_context=True)
    async def xkcd(self, ctx, *, date : str = None):
        """Mencari komik dari XKCD sesuai dengan tanggal (MM-DD-YYYY) atau nomor komik jika ketemu."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if date is None:
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://dilbert.com\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}dilbert [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randilbert` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        if not self.canDisplay(server):
            return
            
        #if not date:
        #    # Auto to today's date
        #    date = dt.datetime.today().strftime("%m-%d-%Y")
            
        if not self.dateIsValid(date):
            # If it's an int - let's see if it fits
            try:
                date = int(date)
            except:
                em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                                   "> http://xkcd.com/\n"
                                                                   "> Sesuai tanggal yang di tentukan\n> \n"
                                                                   "> **Panduan Pengunaan**\n"
                                                                   "> `{}xkcd [tanggal MM-DD-YYYY]`\n"
                                                                   "> atau\n"
                                                                   "> `{}randxkcd` untuk mencari komik secara random"
                                                                   .format(ctx.prefix,
                                                                           ctx.prefix))
                em.set_author(name = "Help command xkcd", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
                em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
                msg = em
                await channel.send(embed = msg)
                return
            # Must be a comic number
            archiveURL = "http://xkcd.com/archive/"
            archiveHTML = await ComicHelper.getImageHTML(archiveURL)
            newest = int(ComicHelper.getNewestXKCD(archiveHTML))
            if int(date) > int(newest) or int(date) < 1:
                em = discord.Embed(color = 0XFF8C00, description = "> Nomor komik harus dari `1` sampai `{}`\n> \n"
                                                                   "> Kalau kamu gak mau ribet gunakan `{}randxkcd` untuk mencari komik secara random"
                                                                   .format(newest,
                                                                           ctx.prefix))
                em.set_author(name = "Komik tidak ditemukan", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
                em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
                msg = em
                await channel.send(embed = msg)
                return
            comicURL = "/" + str(date) + "/"
        else:
            # Can't be after this date.
            todayDate = dt.datetime.today().strftime("%m-%d-%Y")
            # Can't be before this date.
            firstDate = "01-01-2006"

            if not self.isDateBetween(date, firstDate, todayDate):
                em = discord.Embed(color = 0XFF8C00, description = "> Tanggal tidak ditemukan\n"
                                                                   f"> Kamu harus mencari tanggal dari `{firstDate}`\n"
                                                                   f"> sampai tanggal `{todayDate}`\n> \n"
                                                                   f"> Kalau kamu gak mau ribet gunakan `{ctx.prefix}randxkcd` untuk mencari komik secara random"
                                                                   .format(firstDate,
                                                                           todayDate))
                em.set_author(name = "Help command xkcd", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
                em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
                msg = em
                await channel.send(embed = msg)
                return
            # Get date in a dict (Month, Day, Year)
            dateDict = self.dateDict(date)
            # Get URL
            archiveURL = "http://xkcd.com/archive/"
            archiveHTML = await ComicHelper.getImageHTML(archiveURL)

            xkcdDate = "{}-{}-{}".format(int(dateDict['Year']), int(dateDict['Month']), int(dateDict['Day']))
            comicURL = ComicHelper.getXKCDURL( archiveHTML, xkcdDate )
        
        if not comicURL:
            em = discord.Embed(color = 0XFF8C00, description = "> Komik tidak ditemukan untuk tanggal {}\n> \n"
                                                               "> Kamu harus mencari tanggal dari `{}`\n"
                                                               "> sampai tanggal `{}`\n> \n"
                                                               "> Kalau kamu gak mau ribet gunakan `{}randxkcd` untuk mencari komik secara random"
                                                               .format(date,
                                                                       firstDate,
                                                                       todayDate,
                                                                       ctx.prefix))
            em.set_author(name = "Komik tidak ditemukan", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        comicNumber = comicURL.replace('/', '').strip()
        comicURL = "http://xkcd.com" + comicURL

        # now we get the actual comic info
        imageHTML = await ComicHelper.getImageHTML(comicURL)
        imageURL = ComicHelper.getXKCDImageURL(imageHTML)
        imageText = ComicHelper.getXKCDImageText(imageHTML)
        imageDisplayName = ComicHelper.getXKCDImageTitle(imageHTML)
        title = '{} *({})*'.format(imageDisplayName, comicNumber)
        # Download Image
        await Message.Embed(title=title, image=imageURL, url=imageURL, color=0XFF8C00, description=imageText).send(ctx)
        # await GetImage.get(ctx, imageURL, title)
        
        
      # ################### #
     # Cyanide & Happiness #    
    # ################### # 
        
    @commands.command(pass_context=True)
    async def randcyanide(self, ctx):
        """Mencari komik dari Cyanide & Happiness secara random."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if not self.canDisplay(server):
            return
        
        # Can't be after this date.
        todayDate = dt.datetime.today().strftime("%m-%d-%Y")
        # Can't be before this date.
        firstDate = "01-26-2005"

        # Get a random Julian date between the first comic and today
        gotComic = False
        tries = 0
        while not gotComic:
        
            if tries >= 10:
                break
                        
            date = self.getRandDateBetween(firstDate, todayDate)

            # Get Arvhive URL
            getURL = "http://explosm.net/comics/archive/" + date['Year'] + "/" + date['Month']
        
            # Retrieve html and info
            imageHTML = await ComicHelper.getImageHTML(getURL)
            if imageHTML:
                imagePage = ComicHelper.getCHURL(imageHTML, date['Year'] + "." + date['Month'] + "." + date['Day'])
                if imagePage:
                    comicHTML = await ComicHelper.getImageHTML(imagePage)
                    if comicHTML:
                        imageURL  = ComicHelper.getCHImageURL( comicHTML )
                        if imageURL:
                            gotComic = True
                
            tries += 1
            
        if tries >= 10:
            msg = 'Gagal menemukan link, coba lagi nanti.'
            await channel.send(msg)
            return
            
        imageDisplayName = "Cyanide & Happiness Comic tanggal " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
        # Download Image
        await Message.Embed(title=imageDisplayName, image=imageURL.strip(), url=imageURL.strip(), color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL.strip(), imageDisplayName)



    @commands.command(pass_context=True)
    async def cyanide(self, ctx, *, date : str = None):
        """Mencari komik Cyanide & Happiness sesuai tanggal yang kamu cari (MM-DD-YYYY) jika ketemu."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if date == None:
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://dilbert.com\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}dilbert [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randilbert` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        if not self.canDisplay(server):
            return
            
        if not date:
            # Auto to today's date
            date = dt.datetime.today().strftime("%m-%d-%Y")
            
        if not self.dateIsValid(date):
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://explosm.net/\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}cyanide [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randcyanide` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command cyanide", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        # Can't be after this date.
        todayDate = dt.datetime.today().strftime("%m-%d-%Y")
        # Can't be before this date.
        firstDate = "01-26-2005"

        if not self.isDateBetween(date, firstDate, todayDate):
            em = discord.Embed(color = 0XFF8C00, description = "> Tanggal tidak ditemukan\n"
                                                               "> Kamu harus mencari tanggal dari `{}`\n"
                                                               "> sampai tanggal `{}`\n> \n"
                                                               "> Kalau kamu gak mau ribet gunakan `{}randcyanided` untuk mencari komik secara random"
                                                               .format(firstDate,
                                                                todayDate,
                                                                ctx.prefix))
            em.set_author(name = "Help command cyanide", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        dateDict = self.dateDict(date)  
        # Get Arvhive URL
        getURL = "http://explosm.net/comics/archive/" + dateDict['Year'] + "/" + dateDict['Month']

        gotComic = False
        imageHTML = await ComicHelper.getImageHTML(getURL)
        if imageHTML:
            imagePage = ComicHelper.getCHURL(imageHTML, dateDict['Year'] + "." + dateDict['Month'] + "." + dateDict['Day'])
            if imagePage:
                comicHTML = await ComicHelper.getImageHTML(imagePage)
                if comicHTML:
                    imageURL  = ComicHelper.getCHImageURL( comicHTML )
                    if imageURL:
                        gotComic = True
        
        if not gotComic:
            msg = 'Tidak dapat menemukan komik untuk tanggal *{}*'.format(date)
            await channel.send(msg)
            return
        
        imageDisplayName = "Cyanide & Happiness Comic tanggal " + dateDict['Month'] + "-" + dateDict['Day'] + "-" + dateDict['Year']
        # Download Image
        await Message.Embed(title=imageDisplayName, image=imageURL.strip(), url=imageURL.strip(), color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL.strip(), imageDisplayName)
        
        
      # ############### #
     # Calvin & Hobbes #
    # ############### #
    
    @commands.command(pass_context=True)
    async def randcalvin(self, ctx):
        """Mencari komik Calvin & Hobbes."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if not self.canDisplay(server):
            return

        # Can't be after this date.
        todayDate = "12-31-1995"
        # Can't be before this date.
        firstDate = "11-18-1985"

        gotComic = False
        tries = 0
        while not gotComic:
        
            if tries >= 10:
                break
                        
            date = self.getRandDateBetween(firstDate, todayDate)
            # Get URL
            # getURL = "http://marcel-oehler.marcellosendos.ch/comics/ch/" + date['Year'] + "/" + date['Month'] + "/" + date['Year'] + date['Month'] + date['Day'] + ".gif"
            getURL = "http://downloads.esbasura.com/comics/Calvin%20and%20Hobbes/" + date["Year"] + "/" + "ch" + date["Year"][2:] + date["Month"] + date["Day"] + ".gif"

            # Retrieve html and info
            imageHTML = await ComicHelper.getImageHTML(getURL.strip(), "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        
            if imageHTML:
                imageURL  = getURL
                gotComic = True
                
            tries += 1
            
        if tries >= 10:
            msg = 'Failed to find working link.'
            await channel.send(msg)
            return
            
        imageDisplayName = "Komik Calvin & Hobbes tanggal " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
        # Download Image
        await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL, imageDisplayName)



    @commands.command(pass_context=True)
    async def calvin(self, ctx, *, date : str = None):
        """Mencari komik Calvin & Hobbes sesuai tanggal yang kamu cari (MM-DD-YYYY) if found."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if date == None:
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://dilbert.com\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}dilbert [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randilbert` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        if not self.canDisplay(server):
            return
            
        if not date:
            # Auto to the last Calvin & Hobbes comic
            date = "12-31-1995"
            
        if not self.dateIsValid(date):
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://downloads.esbasura.com/comics/Calvin%20and%20Hobbes/\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}calvin [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randcalvin` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command calvin", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        # Can't be after this date.
        todayDate = "12-31-1995"
        # Can't be before this date.
        firstDate = "11-18-1985"

        if not self.isDateBetween(date, firstDate, todayDate):
            em = discord.Embed(color = 0XFF8C00, description = "> Tanggal tidak ditemukan\n"
                                                               f"> Kamu harus mencari tanggal dari `{firstDate}`\n"
                                                               f"> sampai tanggal `{todayDate}`\n> \n"
                                                               f"> Kalau kamu gak mau ribet gunakan `{ctx.prefix}randcalvin` untuk mencari komik secara random"
                                                               .format(firstDate,
                                                                       todayDate,
                                                                       ctx.prefix))
            em.set_author(name = "Help command calvin", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        dateDict = self.dateDict(date)
        # Get URL
        # getURL = "http://marcel-oehler.marcellosendos.ch/comics/ch/" + dateDict['Year'] + "/" + dateDict['Month'] + "/" + dateDict['Year'] + dateDict['Month'] + dateDict['Day'] + ".gif"
        getURL = "http://downloads.esbasura.com/comics/Calvin%20and%20Hobbes/" + dateDict["Year"] + "/" + "ch" + dateDict["Year"][2:] + dateDict["Month"] + dateDict["Day"] + ".gif"

        # Retrieve html and info
        imageHTML = await ComicHelper.getImageHTML(getURL, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        
        if not imageHTML:
            msg = 'Tidak dapat mencari komik tanggal *{}*'.format(date)
            await channel.send(msg)
            return

        imageDisplayName = "Komik Calvin & Hobbes tanggal " + dateDict['Month'] + "-" + dateDict['Day'] + "-" + dateDict['Year']
        # Download Image
        await Message.Embed(title=imageDisplayName, image=getURL, url=getURL, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, getURL, imageDisplayName)
        
        
      # ####################### #
     # Garfield Minus Garfield #
    # ####################### #
    
    @commands.command(pass_context=True)
    async def randgmg(self, ctx):
        """Mencari Komik Garfield Minus Garfield secara random."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if not self.canDisplay(server):
            return

        # Can't be after this date.
        todayDate = dt.datetime.today().strftime("%m-%d-%Y")
        # Can't be before this date.
        firstDate = "02-13-2008"

        # Get a random Julian date between the first comic and today
        gotComic = False
        tries = 0
        while not gotComic:
        
            if tries >= 10:
                break
                
            date = self.getRandDateBetween(firstDate, todayDate)
            # Get URL
            getURL = "http://garfieldminusgarfield.net/day/" + date['Year'] + "/" + date['Month'] + "/" + date['Day']
            # Retrieve html and info
            imageHTML = await ComicHelper.getImageHTML(getURL)
        
            if imageHTML:
                imageURL  = ComicHelper.getGMGImageURL(imageHTML)
                if imageURL:
                    gotComic = True
                
            tries += 1

        if tries >= 10:
            msg = 'Failed to find working link.'
            await channel.send(msg)
            return
        
        imageDisplayName = "Garfield Minus Garfield Comic for " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
        # Download Image
        await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL, imageDisplayName)



    @commands.command(pass_context=True)
    async def gmg(self, ctx, *, date : str = None):
        """Mencari komik Garfield Minus Garfield dengan tanggal yang kamu cari (MM-DD-YYYY) jika ketemu."""
        
        channel = ctx.message.channel
        author  = ctx.message.author
        server  = ctx.message.guild
        
        if date == None:
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://dilbert.com\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}dilbert [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randilbert` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command dilbert", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return
        
        if not self.canDisplay(server):
            return
            
        if not date:
            # Auto to today
            date = dt.datetime.today().strftime("%m-%d-%Y")
            
        if not self.dateIsValid(date):
            em = discord.Embed(color = 0XFF8C00, description = "> Mencari komik dari\n"
                                                               "> http://downloads.esbasura.com/comics/Calvin%20and%20Hobbes/\n"
                                                               "> Sesuai tanggal yang di tentukan\n> \n"
                                                               "> **Panduan Pengunaan**\n"
                                                               "> `{}gmg [tanggal MM-DD-YYYY]`\n"
                                                               "> atau\n"
                                                               "> `{}randgmg` untuk mencari komik secara random"
                                                              .format(ctx.prefix,
                                                                      ctx.prefix))
            em.set_author(name = "Help command gmg", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        # Can't be after this date.
        todayDate = dt.datetime.today().strftime("%m-%d-%Y")
        # Can't be before this date.
        firstDate = "02-13-2008"

        if not self.isDateBetween(date, firstDate, todayDate):
            em = discord.Embed(color = 0XFF8C00, description =  "> Tanggal tidak ditemukan\n"
                                                               f"> Kamu harus mencari tanggal dari `{firstDate}`\n"
                                                               f"> sampai tanggal `{todayDate}`\n> \n"
                                                               f"> Kalau kamu gak mau ribet gunakan `{ctx.prefix}randgmg` untuk mencari komik secara random"
                                                               .format(firstDate,
                                                                       todayDate,
                                                                       ctx.prefix))
            em.set_author(name = "Help command gmg", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        dateDict = self.dateDict(date)

        # Get URL
        getURL = "http://garfieldminusgarfield.net/day/" + dateDict['Year'] + "/" + dateDict['Month'] + "/" + dateDict['Day']
        
        # Retrieve html and info
        imageHTML = await ComicHelper.getImageHTML(getURL)
        
        # Comment out to test
        '''if imageHTML == None:
            msg = 'No comic found for *{}*'.format(date)
            await channel.send(msg)
            return'''
        
        imageURL  = ComicHelper.getGMGImageURL(imageHTML)

        if not imageURL:
            em = discord.Embed(color = 0XFF8C00, description = "> Komik tidak ditemukan untuk tanggal {}\n> \n"
                                                               "> Kamu harus mencari tanggal dari `{}`\n"
                                                               "> sampai tanggal ``{}``\n> \n"
                                                               "> Kalau kamu gak mau ribet gunakan `{}randgmg` untuk mencari komik secara random"
                                                               .format(date,
                                                                       firstDate,
                                                                       todayDate.
                                                                       ctx.prefix))
            em.set_author(name = "Komik tidak ditemukan", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            msg = em
            await channel.send(embed = msg)
            return

        imageDisplayName = "Komik Garfield Minus Garfield tanggal " + dateDict['Month'] + "-" + dateDict['Day'] + "-" + dateDict['Year']
        # Download Image
        await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
        # await GetImage.get(ctx, imageURL, imageDisplayName)
        
        
      # ######## #
     # Garfield #
    # ######## #
        
    # @commands.command(pass_context=True)
    # async def randgarfield(self, ctx):
    #     """Randomly picks and displays a Garfield comic."""
        
    #     channel = ctx.message.channel
    #     author  = ctx.message.author
    #     server  = ctx.message.guild
        
    #     if not self.canDisplay(server):
    #         return

    #     # Can't be after this date.
    #     todayDate = dt.datetime.today().strftime("%m-%d-%Y")
    #     # Can't be before this date.
    #     firstDate = "06-19-1978"

    #     # Get a random Julian date between the first comic and today
    #     gotComic = False
    #     tries = 0
    #     while not gotComic:
        
    #         if tries >= 10:
    #             break
                
    #         date = self.getRandDateBetween(firstDate, todayDate)
    #         # Get URL
    #         getURL = "https://garfield.com/comic/" + date['Year'] + "/" + date['Month'] + "/" + date['Day']
    #         # Retrieve html and info
    #         imageHTML = await ComicHelper.getImageHTML(getURL)
        
    #         if imageHTML:
    #             imageURL  = ComicHelper.getGImageURL(imageHTML)
    #             if imageURL:
    #                 gotComic = True
                
    #         tries += 1

    #     if tries >= 10:
    #         msg = 'Failed to find working link.'
    #         await channel.send(msg)
    #         return
        
    #     imageDisplayName = "Garfield Comic for " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
    #     # Download Image
    #     await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
    #     # await GetImage.get(ctx, imageURL, imageDisplayName)
        
    # @commands.command(pass_context=True)
    # async def garfield(self, ctx, *, date : str = None):
    #     """Displays the Garfield comic for the passed date (MM-DD-YYYY) if found."""
        
    #     channel = ctx.message.channel
    #     author  = ctx.message.author
    #     server  = ctx.message.guild
        
    #     if not self.canDisplay(server):
    #         return
            
    #     if not date:
    #         # Auto to today
    #         date = dt.datetime.today().strftime("%m-%d-%Y")
            
    #     if not self.dateIsValid(date):
    #         msg = 'Usage: `{}garfield "[date MM-DD-YYYY]"`'.format(ctx.prefix)
    #         await channel.send(msg)
    #         return

    #     # Can't be after this date.
    #     todayDate = dt.datetime.today().strftime("%m-%d-%Y")
    #     # Can't be before this date.
    #     firstDate = "06-19-1978"

    #     if not self.isDateBetween(date, firstDate, todayDate):
    #         msg = "Date out of range. Must be between {} and {}".format(firstDate, todayDate)
    #         await channel.send(msg)
    #         return

    #     dateDict = self.dateDict(date)

    #     # Get URL
    #     getURL = "https://garfield.com/comic/" + dateDict['Year'] + "/" + dateDict['Month'] + "/" + dateDict['Day']
        
    #     # Retrieve html and info
    #     imageHTML = await ComicHelper.getImageHTML(getURL)
        
    #     # Comment out to test
    #     '''if imageHTML == None:
    #         msg = 'No comic found for *{}*'.format(date)
    #         await channel.send(msg)
    #         return'''
        
    #     imageURL  = ComicHelper.getGImageURL(imageHTML)

    #     if not imageURL:
    #         msg = 'No comic found for *{}*'.format(date)
    #         await channel.send(msg)
    #         return

    #     imageDisplayName = "Garfield Comic for " + dateDict['Month'] + "-" + dateDict['Day'] + "-" + dateDict['Year']
    #     # Download Image
    #     await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
    #     # await GetImage.get(ctx, imageURL, imageDisplayName)
        
        
    #   # ####### #   
    #  # Peanuts #
    # # ####### #
    
    # @commands.command(pass_context=True)
    # async def randpeanuts(self, ctx):
    #     """Randomly picks and displays a Peanuts comic."""
        
    #     channel = ctx.message.channel
    #     author  = ctx.message.author
    #     server  = ctx.message.guild
        
    #     if not self.canDisplay(server):
    #         return

    #     # Can't be after this date.
    #     todayDate = dt.datetime.today().strftime("%m-%d-%Y")
    #     # Can't be before this date.
    #     firstDate = "10-02-1950"

    #     # Get a random Julian date between the first comic and today
    #     gotComic = False
    #     tries = 0
    #     while not gotComic:
        
    #         if tries >= 10:
    #             break
                
    #         date = self.getRandDateBetween(firstDate, todayDate)
    #         # Get URL
    #         getURL = "http://www.gocomics.com/peanuts/" + date['Year'] + "/" + date['Month'] + "/" + date['Day']
    #         # Retrieve html and info
    #         imageHTML = await ComicHelper.getImageHTML(getURL)
        
    #         if imageHTML:
    #             imageURL  = ComicHelper.getPeanutsImageURL(imageHTML)
    #             if imageURL:
    #                 gotComic = True
                
    #         tries += 1

    #     if tries >= 10:
    #         msg = 'Failed to find working link.'
    #         await channel.send(msg)
    #         return
        
    #     imageDisplayName = "Peanuts Comic for " + date['Month'] + "-" + date['Day'] + "-" + date['Year']
    #     # Download Image
    #     await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
    #     # await GetImage.get(ctx, imageURL, imageDisplayName)
        
    # @commands.command(pass_context=True)
    # async def peanuts(self, ctx, *, date : str = None):
    #     """Displays the Peanuts comic for the passed date (MM-DD-YYYY) if found."""
        
    #     channel = ctx.message.channel
    #     author  = ctx.message.author
    #     server  = ctx.message.guild
        
    #     if not self.canDisplay(server):
    #         return
            
    #     if not date:
    #         # Auto to today
    #         date = dt.datetime.today().strftime("%m-%d-%Y")
            
    #     if not self.dateIsValid(date):
    #         msg = 'Usage: `{}peanuts "[date MM-DD-YYYY]"`'.format(ctx.prefix)
    #         await channel.send(msg)
    #         return

    #     # Can't be after this date.
    #     todayDate = dt.datetime.today().strftime("%m-%d-%Y")
    #     # Can't be before this date.
    #     firstDate = "10-02-1950"

    #     if not self.isDateBetween(date, firstDate, todayDate):
    #         msg = "Date out of range. Must be between {} and {}".format(firstDate, todayDate)
    #         await channel.send(msg)
    #         return

    #     dateDict = self.dateDict(date)

    #     # Get URL
    #     getURL = "http://www.gocomics.com/peanuts/" + dateDict['Year'] + "/" + dateDict['Month'] + "/" + dateDict['Day']
        
    #     # Retrieve html and info
    #     imageHTML = await ComicHelper.getImageHTML(getURL)
        
    #     # Comment out to test
    #     '''if imageHTML == None:
    #         msg = 'No comic found for *{}*'.format(date)
    #         await channel.send(msg)
    #         return'''
        
    #     imageURL  = ComicHelper.getPeanutsImageURL(imageHTML)

    #     if not imageURL:
    #         msg = 'No comic found for *{}*'.format(date)
    #         await channel.send(msg)
    #         return

    #     imageDisplayName = "Peanuts Comic for " + dateDict['Month'] + "-" + dateDict['Day'] + "-" + dateDict['Year']
    #     # Download Image
    #     await Message.Embed(title=imageDisplayName, image=imageURL, url=imageURL, color=0XFF8C00).send(ctx)
    #     # await GetImage.get(ctx, imageURL, imageDisplayName)
