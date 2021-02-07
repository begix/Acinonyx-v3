import asyncio, discord, random, json, time, os, PIL, textwrap, requests
from bs4 import BeautifulSoup as bSoup
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from Cogs import Message, FuzzySearch, GetImage, Nullify, DL, DisplayName

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Humor(bot, settings))

# This module is for random funny things I guess...

class Humor(commands.Cog):

    def __init__(self, bot, settings, listName = "Adjectives.txt"):
        self.bot = bot
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")
        self.settings = settings
        # Setup our adjective list
        self.adj = []
        marks = map(chr, range(768, 879))
        self.marks = list(marks)
        if os.path.exists(listName):
            with open(listName) as f:
                for line in f:
                    self.adj.append(line)
        try: self.image = Image.open('images/dosomething.png')
        except: self.image = Image.new("RGBA",(500,500),(0,0,0,0))
        try: self.s_image = Image.open("images/Stardew.png")
        except: self.s_image = Image.new("RGBA",(319,111),(0,0,0,0))
        self.stardew_gifts = [
            "prismatic shard",
            "seaweed",
            "green algae",
            "diamond",
            "red mushrooms",
            "wool",
            "coal",
            "duck feather",
            "cave carrot",
            "solar essence",
            "vinegar",
            "sweet gem berry",
            "truffle",
            "fish",
            "snail",
            "frozen tear",
            "chicken statue",
            "bone flute",
            "pufferfish",
            "Joja Cola",
            "trash",
            "egg",
            "crispy bass",
            "fish taco",
            "cookie",
            "garlic",
            "weeds",
            "honey",
            "gizmo",
            "cloth",
            "geode"
            ]
        self.stardew_responses = [
            "I'm just here for my annual check-up! Don't worry, I'm not preg... I mean, I'm not sick! Heh.",
            "...I hate this.",
            "Buh... Life.",
            "You wish to date me? After how I treated you at first?",
            "What do you want? Leave me alone.",
            "You!!! Was that some kind of sick prank?! Those are very private!",
            "Did you know that my nephew loves 'Beer'? I gave it to him one year and he wouldn't stop talking about it.",
            "Ugh... that's such a stupid gift.",
            "Don't you have work to do?",
            "I'm just here for the free coffee.",
            "I'll be honest. I don't want to dance with you",
            "Me?... Oh, I'm thankful for... how about I just show you when we get home tonight?",
            "Thanks!",
            "Oh, is it my birthday today? I guess it is. Thanks. This is nice.",
            "I wanted to talk to you in private...",
            "Ew... No.",
            "Sometimes I stop and realize that I'm nothing more than a bag of juicy, squishy flesh.",
            "Ah... an Fish Taco! Thanks.",
            "No u.",
            "Thanks... I hate it.",
            "I really should scrub my floorboards today. I think an algae is starting to form.",
            "That was some way to ring in the new year last night...",
            "You scared me, sneaking into my room like that!",
            "So there you have it. You probably figured I hated this chair.",
            "This... Are you trying to hurt me even more?",
            "I thought we had something special... I guess I was wrong.",
            "This... They gave this to me in Gotoro prison camp. I've been trying to forget about that. *shudder*",
            "If I stay perfectly still, perhaps a resplendent butterfly will bless my nose with a landing.",
            "My basket! Thank you. This means a lot to me.",
            "But... You don't need to try and 'help' me... I know best how to live my own life... okay?",
            "This is a great gift. Thank you!",
            "Oh, a birthday gift! Thank you.",
            "All my customers... Here?!?",
            "Grr... sounds like these raccoons are back again. Filthy varmints...",
            "Sometimes I look for crawdads in the river. Don't tell Aunt Marnie... but I fed one to a cow once."
        ]
                    
    @commands.command(pass_context=True)
    async def zalgo(self, ctx, *, message = None):
        """A͙P̟A̻ I͆N͒I͚ Ċ͙Uͤ͘U̲͋U͉̓Ű̝K̲͑!"""
        if message == None:
            await ctx.send("Usage: `{}zalgo [message]`".format(ctx.prefix))
            return
        # Check if we're suppressing @here and @everyone mentions
        if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
            suppress = True
        else:
            suppress = False
        
        words = message.split()
        try:
            iterations = int(words[len(words)-1])
            words = words[:-1]
        except Exception:
            iterations = 1
            
        if iterations > 100:
            iterations = 100
        if iterations < 1:
            iterations = 1
            
        zalgo = " ".join(words)
        for i in range(iterations):
            if len(zalgo) > 2000:
                break
            zalgo = self._zalgo(zalgo)
        
        zalgo = zalgo[:2000]

        # Check for suppress
        if suppress:
            zalgo = Nullify.clean(zalgo)
        await Message.Message(message=zalgo).send(ctx)
        #await ctx.send(zalgo)
        
    def _zalgo(self, text):
        words = text.split()
        zalgo = ' '.join(''.join(c + ''.join(random.choice(self.marks)
                for _ in range(i // 2 + 1)) * c.isalnum()
                for c in word)
                for i, word in enumerate(words))
        return zalgo

    # @commands.command(pass_context=True)
    # async def holy(self, ctx, *, subject : str = None):
    #   """Time to backup the Batman!"""
        
    #   if subject == None:
    #       await ctx.channel.send("Usage: `{}holy [subject]`".format(ctx.prefix))
    #       return
        
    #   # Check if we're suppressing @here and @everyone mentions
    #   if self.settings.getServerStat(ctx.message.guild, "SuppressMentions"):
    #       suppress = True
    #   else:
    #       suppress = False
        
    #   matchList = []
    #   for a in self.adj:
    #       if a[:1].lower() == subject[:1].lower():
    #           matchList.append(a)
        
    #   if not len(matchList):
    #       # Nothing in there - get random entry
    #       # msg = "*Whoah there!* That was *too* holy for Robin!"
    #       word = random.choice(self.adj)
    #       word = word.strip().capitalize()
    #       subject = subject.strip().capitalize()
    #       msg = "*Holy {} {}, Batman!*".format(word, subject)
    #   else:
    #       # Get a random one
    #       word = random.choice(matchList)
    #       word = word.strip().capitalize()
    #       subject = subject.strip().capitalize()
    #       msg = "*Holy {} {}, Batman!*".format(word, subject)
        
    #   # Check for suppress
    #   if suppress:
    #       msg = Nullify.clean(msg)
    #   await ctx.channel.send(msg)
        
    # @commands.command(pass_context=True)
    # async def fart(self, ctx):
    #   """PrincessZoey :P"""
    #   fartList = ["Poot", "Prrrrt", "Thhbbthbbbthhh", "Plllleerrrrffff", "Toot", "Blaaaaahnk", "Squerk"]
    #   randnum = random.randint(0, len(fartList)-1)
    #   msg = '{}'.format(fartList[randnum])
    #   await ctx.channel.send(msg)
        
    # @commands.command(pass_context=True)
    # async def french(self, ctx):
    #   """Speaking French... probably..."""
    #   fr_list = [ "hon", "fromage", "baguette" ]
    #   punct   = [ ".", "!", "?", "...", "!!!", "?!" ]
    #   fr_sentence = []
    #   for i in range(random.randint(3, 20)):
    #       fr_sentence.append(random.choice(fr_list))
    #   # Capitalize the first letter of the first word
    #   fr_sentence[0] = fr_sentence[0][:1].upper() + fr_sentence[0][1:]
    #   totally_french = " ".join(fr_sentence) + random.choice(punct)
    #   await ctx.send(totally_french)

    # @commands.command(pass_context=True)
    # async def german(self, ctx):
    #   """Speaking German... probably..."""
    #   de_list = [ "BIER", "sauerkraut", "auto", "weißwurst", "KRANKENWAGEN" ]
    #   punct   = [ ".", "!", "?", "...", "!!!", "?!" ]
    #   de_sentence = []
    #   for i in range(random.randint(3, 20)):
    #       de_sentence.append(random.choice(de_list))
    #   if random.randint(0,1):
    #       # Toss "rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz" in there somewhere
    #       de_sentence[random.randint(0,len(de_sentence)-1)] = "rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz"
    #   # Capitalize the first letter of the first word
    #   de_sentence[0] = de_sentence[0][:1].upper() + de_sentence[0][1:]
    #   totally_german = " ".join(de_sentence) + random.choice(punct)
    #   await ctx.send(totally_german)

    def canDisplay(self, server):
        # Check if we can display images
        lastTime = int(self.settings.getServerStat(server, "LastPicture", 0))
        threshold = int(self.settings.getServerStat(server, "PictureThreshold", 0))
        if not GetImage.canDisplay( lastTime, threshold ):
            # await self.bot.send_message(channel, 'Too many images at once - please wait a few seconds.')
            return False
        
        # If we made it here - set the LastPicture method
        self.settings.setServerStat(server, "LastPicture", int(time.time()))
        return True

    @commands.command(pass_context=True)
    async def memetemps(self, ctx):
        """Meme template"""
        url = "https://api.imgflip.com/get_memes"
        result_json = await DL.async_json(url)
        templates = result_json["data"]["memes"]
        confirm = ['ya']
        Msg = await ctx.send("Command ini akan mengirimkan 4 halaman embed ke private message kamu.\nKetik `ya` untuk melanjutkan")
        try:
            msg = await self.bot.wait_for('message', timeout=15, check=lambda msg: msg.author == ctx.author)
        except:
            await Msg.delete()
            return await ctx.send(f'{ctx.author.name}\nWaktu habis, command mu telah dibatalkan', delete_after=10)
        
        message = str(msg.content.lower())

        if message not in confirm and message not in ['ya']:
            await Msg.delete()
            return await ctx.send(f'{ctx.author.name}\nCommand dibatalkan.\nnKamu memasukan konfirmasi yang salah', delete_after=10)

        templates_string_list = []
        fields = []
        for template in templates:
            fields.append({ "name" : template["name"], "value" : "`" + str(template["id"]) + "`", "inline" : False })
        await Msg.delete()
        await ctx.send("{}\nlist meme template telah dikirim ke private message mu".format(ctx.author.mention))
        await Message.Embed(title="Meme Templates", fields=fields).send(ctx)

    @commands.command(pass_context=True)
    async def meme(self, ctx, template_id = None, text_zero = None, text_one = None):
        """Meme generator!
        Kamu dapat melihat list template meme dengan command `acx!memetemps`.

        jika kalimat/template dipisahkan dengan spasi, harus menggunakan tanda kutip (\").

        Contoh:
        • acx!meme [template/id meme] [text1] [text2]
        • acx!meme 163573 \"BACOT\"
        • acx!meme \"Imagination Spongebob\" \"BACOT\""""

        if not self.canDisplay(ctx.message.guild):
            return

        if text_one == None:
            # Set as space if not included
            text_one = " "

        if template_id == None or text_zero == None or text_one == None:
            msg =  "> **Panduan penggunaan**\n"
            msg += "> `{}meme [template/id meme] [text#1] [text#2]`\n".format(ctx.prefix)
            msg += "> **Contoh**\n"
            msg += "> • `{}meme 163573 \"BACOT\"`\n".format(ctx.prefix)
            msg += "> • `{}meme \"Imagination Spongebob\" \"BACOT\" \"LOE!\"`\n> \n".format(ctx.prefix)
            msg += "> list meme bisa dilihat disini\n"
            msg += "> `{}memetemps`".format(ctx.prefix)
            em = discord.Embed(color = 0XFF8C00,
                               description = msg)
            em.set_author(name = "Meme maker", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Request by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.channel.send(embed = em)
            return

        templates = await self.getTemps()

        chosenTemp = None
        msg = ''

        idMatch   = FuzzySearch.search(template_id, templates, 'id', 1)
        if idMatch[0]['Ratio'] == 1:
            # Perfect match
            chosenTemp = idMatch[0]['Item']['id']
        else:
            # Imperfect match - assume the name
            nameMatch = FuzzySearch.search(template_id, templates, 'name', 1)
            chosenTemp = nameMatch[0]['Item']['id']
            if nameMatch[0]['Ratio'] < 1:
                # Less than perfect, still
                msg = 'Mungkin yang kamu maksud *{}*.'.format(nameMatch[0]['Item']['name'])

        url = "https://api.imgflip.com/caption_image"
        payload = {'template_id': chosenTemp, 'username':'CorpBot', 'password': 'pooter123', 'text0': text_zero, 'text1': text_one }
        result_json = await DL.async_post_json(url, payload)
        # json.loads(r.text)
        result = result_json["data"]["url"]
        if msg:
            # result = '{}\n{}'.format(msg, result)
            await ctx.channel.send(msg)
        # Download Image - set title as a space so it disappears on upload
        await Message.Embed(image=result, color=ctx.author).send(ctx)
        # await GetImage.get(ctx, result)

    async def getTemps(self):
        url = "https://api.imgflip.com/get_memes"
        result_json = await DL.async_json(url)
        templates = result_json["data"]["memes"]
        if templates:
            return templates
        return None

    @commands.command()
    async def poke(self, ctx, *, url = None):
        """Poke url/user/attachment gambar."""

        if not self.canDisplay(ctx.guild):
            return
        if url == None and len(ctx.message.attachments) == 0:
            em = discord.Embed(color = 0XFF8C00,
                               description = "> **Panduan**\n"
                                             "> `{}poke [url, user, atau attachment]`"
                                             .format(ctx.prefix))
            em.set_author(name = "Poke", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            await ctx.send(embed=em)
            return
        if url == None:
            url = ctx.message.attachments[0].url
        # Let's check if the "url" is actually a user
        test_user = DisplayName.memberForName(url, ctx.guild)
        if test_user:
            # Got a user!
            url = test_user.avatar_url
            if not len(url):
                url = test_user.default_avatar_url
        image = self.image.copy()
        message = await ctx.send("Mempersiapkan gambar...")
        path = await GetImage.download(url)
        if not path:
            return await message.edit(content="Aku tidak dapat melakukannya sekarang...\npastikan kamu memasukan user, url, atau attachment dengan benar.")
        # We should have the image - let's open it and convert to a single frame
        try:
            img = Image.open(path)
            img = img.convert('RGBA')
            # Let's ensure it's the right size, and place it in the right spot
            t_max   = int(image.width*.38)
            t_ratio = min(t_max/img.width,t_max/img.height)
            t_w = int(img.width*t_ratio)
            t_h = int(img.height*t_ratio)
            img = img.resize((t_w,t_h),resample=PIL.Image.LANCZOS)
            # Paste our other image on top
            image.paste(img,(int(image.width*.6),int(image.height*.98)-t_h),mask=img)
            image.save('images/dosomethingnow.png')
            await ctx.send(file=discord.File(fp='images/dosomethingnow.png'))
            await message.delete()
            os.remove('images/dosomethingnow.png')
        except Exception as e:
            print(e)
            pass
        if os.path.exists(path):
            GetImage.remove(path)

    @commands.command()
    async def stardew(self, ctx, *, user = None):
        """Test keberuntungan mu dengan user lain."""

        # Set some defaults
        name_max_w = 92
        name_max_h = 15
        if not self.canDisplay(ctx.guild):
            return
        # Let's check if the "url" is actually a user
        test_user = DisplayName.memberForName(user, ctx.guild)
        if not test_user:
            em = discord.Embed(color = 0XFF8C00,
                               description = "> **Panduan**\n"
                                             "> `{}stardew [user/member]`"
                                             .format(ctx.prefix))
            em.set_author(name = "Stardew", url = "https://acinonyxesports.com", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\nRequest by : {}".format(ctx.author.name), icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed=em)
        # Got a user!
        user = test_user.avatar_url
        if not len(user):
            user = test_user.default_avatar_url
        # User profile pic needs to be formatted to 64x65 pixels - and the top left corner is at
        # (221,15)
        image = self.s_image.copy()
        if not image.width == 319 or not image.height == 111:
            image = image.resize((319,111),resample=PIL.Image.LANCZOS)
        message = await ctx.send("Gifting *{}* to {}...".format(random.choice(self.stardew_gifts),Nullify.clean(DisplayName.name(test_user))))
        path = await GetImage.download(user)
        if not path:
            return await message.edit(content="Aku tidak dapat melakukannya sekarang...\nPastikan kamu memasukan user/member dengan benar.")
        # We should have the image - let's open it and convert to a single frame
        try:
            img = Image.open(path)
            img = img.convert('RGBA')
            # Let's ensure it's the right size, and place it in the right spot
            img = img.resize((64,65))
            # Paste our other image on top
            image.paste(img,(221,15),mask=img)
            # Write the user's name in the name box - starts at (209,99)
            d = ImageDraw.Draw(image)
            name_text = DisplayName.name(test_user)
            name_size = name_max_h # max size for the name to fit
            t_w,t_h = d.textsize(name_text,font=ImageFont.truetype("fonts/stardew.ttf",name_size))
            if t_w > name_max_w:
                name_size = int(t_h*(name_max_w/t_w))
                t_w,t_h = d.textsize(name_text,font=ImageFont.truetype("fonts/stardew.ttf",name_size))
            d.text((210+(88-t_w)/2,88+(12-t_h)/2),DisplayName.name(test_user),font=ImageFont.truetype("fonts/stardew.ttf",name_size),fill=(86,22,12))
            # Get the response - origin is (10,10), each row height is 14
            rows = textwrap.wrap(
                random.choice(self.stardew_responses),
                30,
                break_long_words=True,
                replace_whitespace=False
                )
            for index,row in enumerate(rows[:6]):
                d.text((11+2,10+14*index),row,font=ImageFont.truetype("fonts/stardew.ttf",15),fill=(86,22,12))
            # Resize to triple and save
            image = image.resize((319*3,111*3),PIL.Image.NEAREST)
            image.save('images/Stardewnow.png')
            await ctx.send(file=discord.File(fp='images/Stardewnow.png'))
            await message.delete(delay=2)
            os.remove('images/Stardewnow.png')
        except Exception as e:
            print(e)
            pass
        if os.path.exists(path):
            GetImage.remove(path)

    @commands.command()
    async def gameinfo(self, ctx, *, game = None):
      """Command ini masih dalam tahap pengembangan."""
      try:
        game = game.replace(" ","-")
        r = requests.get("https://gamesystemrequirements.com/game/{}".format(game))
        s = bSoup(r.text, "html.parser")

        gtitle = s.find("div", class_="game_head_title").text
        grow = [a.text for a in s.find_all("div", class_="game_head_details_row")]
        sysreqrowttl = [a.find("div", class_="tbl").b.text.replace(":","") for a in s.find_all("div", class_="srb_row") if a.find("div", class_="tbl") is not None]

        sysreqrowres = []
        for a in s.find_all("div", class_="srb_row"):
            if a.find("div", style="display:table-cell") is not None:
                for c in a.find_all("div", style="display:table-cell"):
                    sysreqrowres.append(c.text)

        sysmin = {}
        sysrec = {}
        for a,b,c in zip(sysreqrowttl, sysreqrowres[::2],sysreqrowres[1::2]):
            sysmin[a] = b
            sysrec[a] = c
            #sysmin |= {a:b}
            #sysrec |= {a:c}

        data = {
         "status": "sucess",
         "copyright": "[ACX] NvStar",
         "source": "https://gamesystemrequirements.com",
         "result": {
          "game": gtitle,
          "release-date": grow[0].replace("Release Date: ", ""),
          "average": grow[1].replace("Sys. Reqs.: ", ""),
          "popularity": grow[2].replace("Popularity: ", ""),
          "reviews": grow[3].replace("Reviews: ", ""),
          "genres": grow[4].replace("Genre: ", ""),
          "developer": grow[5].replace("Developer: ", ""),
          "publisher": grow[6].replace("Publisher: ", ""),
          "specifications": {
           "minimum": sysmin,
           "recommended": sysrec
          }
         }
        }

        data = json.dumps(data,indent=4)
        print(data)
        data = json.loads(data)
        
        msg =  "Informasi game **{}**".format(data["result"]["game"])
        msg += "```\n"
        msg += "Developer  :: {}\n".format(data["result"]["developer"])
        msg += "Publisher  :: {}\n".format(data["result"]["publisher"])
        msg += "Release    :: {}\n".format(data["result"]["release-date"])
        msg += "Sys. Reqs  :: {}\n".format(data["result"]["average"])
        msg += "Popularity :: {}\n".format(data["result"]["popularity"])
        msg += "Reviews    :: {}\n".format(data["result"]["reviews"])
        msg += "\n```"
        em = discord.Embed(color = 0XFF8C00, description = msg)
        
        val =  "```\n"
        val += "CPU        :: {}\n".format(data["result"]["specifications"]["minimum"]["CPU"])
        val += "RAM        :: {}\n".format(data["result"]["specifications"]["minimum"]["RAM"])
        val += "GPU        :: {}\n".format(data["result"]["specifications"]["minimum"]["GPU"])
        val += "DX         :: {}\n".format(data["result"]["specifications"]["minimum"]["DX"])
        val += "Store      :: {}\n".format(data["result"]["specifications"]["minimum"]["Store"])
        val += "```"
        em.add_field(name = "**Minimum Requirements**", value = val)
        
        val =  "```\n"
        val += "CPU        :: {}\n".format(data["result"]["specifications"]["recommended"]["CPU"])
        val += "RAM        :: {}\n".format(data["result"]["specifications"]["recommended"]["RAM"])
        val += "GPU        :: {}\n".format(data["result"]["specifications"]["recommended"]["GPU"])
        val += "DX         :: {}\n".format(data["result"]["specifications"]["recommended"]["DX"])
        val += "Store      :: {}\n".format(data["result"]["specifications"]["recommended"]["Store"])
        val += "```"
        em.add_field(name = "**Recommended Requirements**", value = val, inline = False)
        await ctx.send(embed = em)
      except Exception as e:
          print(e)
          msg = "┐(￣ヘ￣;)┌\nAku tidak dapat menemukan game *`{}`* yang kamu cari "
          em = discord.Embed(color = 0XFF8C00 ,description = msg)
          await ctx.send(embed = em)