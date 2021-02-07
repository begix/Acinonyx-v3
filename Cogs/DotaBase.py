import discord
from discord.ext import commands
from Cogs        import Utils
from Cogs        import Settings



def setup(bot):
    settings = bot.get_cog("Settings")
    bot.add_cog(DotaBase(bot, settings))

class DotaBase(commands.Cog):

    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    @commands.command()
    async def hero(self, ctx, *, hero = None):
        """Mencari informasi seputar hero DOTA 2.
        Kamu dapat menggunakan command ini dengan option:
        • Nama hero
        • Hero ID

        **Contoh**
        • acx hero sf
        • acx hero inker
        • acx hero furi"""
        print("Command hero dialihkan ke MangoByte")
        
    @commands.command()
    async def item(self, ctx, *, item = None):
        """Mencari informasi seputar item DOTA 2
        
        **Contoh:**
        • acx item shadow blade
        • acx item tango"""
        print("Command item dialihkan ke MangoByte")
        
    @commands.command()
    async def ability(self, ctx, ability = None):
        """Mencari informasi seputar ability hero DOTA 2
        
        **Contoh:**
        • acx ability rocket flare
        • acx ability laser
        • acx ability sprout"""
        print("Command ability dialihkan ke MangoByte")

    @commands.command()
    async def talents(self, ctx, *, hero = None):
        """Mencari informasi talent dari hero DOTA 2.
        Kamu dapat menggunakan command ini dengan option:
        • Nama hero
        • Hero ID

        **Contoh:**
        `acx talents shadow fiend`"""
        print("Command talent dialihkan ke MangoByte")

    @commands.command()
    async def lore(self, ctx, *, name = None):
        """Mencari lore/knowledge (pengetahuan) dari hero, ability, item dalam game DOTA 2
        Jika tidak memasukan [name] aku akan memberikan secara random

        **Contoh:**
        • acx lore bristleback
        • acx lore shadow blade
        • acx lore venomous gale"""
        print("Command lore dialihkan ke MangoByte")

    @commands.command()
    async def leveledstats(self, ctx, *, hero = None):
        """Melihat informasi hero DOTA 2 pada level yang ditentukan.
        Jika tidak memasukan level, aku akan memberikan status hero level 1

        **Contoh:**
        acx leveledstats tinker
        acx leveledstats shaker lvl 2
        acx leveledstats level 28 shaman"""
        print("Command leveledstats dialihkan ke MangoByte")

    @commands.command()
    async def courage(self, ctx, *, hero = None):
        """Kamu ingin menantang teman mu?
        Membuat tantangan dengan random build hero DOTA 2
        (atau kamu dapat memilihi hero) dan random set item

        **Contoh:**
        acx courage
        acx courage shadow fiend"""
        print("Command courage dialihkan ke MangoByte")

    @commands.command()
    async def herotable(self, ctx, *, table_args = None):
        """Menampilkan urutan table dari hero DOTA 2 dan statusnya.
        
        Table statistik hero menampilkan status nilai tertinggi yang ditentukan

        **Contoh:**
        acx herotable dps
        acx herotable health lvl 30
        acx herotable attack speed level 21 descending
        """
        print("Command herotable dialihkan ke MangoByte")

    @commands.command(aliases=["neutrals", "neutraltier"])
    async def neutralitems(self, ctx, *, tier = None):
        """Menampilkan semua neutral item DOTA 2

        Jika kamu memasukan tier yang ditentukan, aku akan menampilkan item dalam tier tersebut beserta namanya
        
        **Contoh:**
        acx neutralitems
        acx neutralitems tier 5
        acx neutralitems 3"""
        print("Command herotable dialihkan ke MangoByte")
        
    @commands.command(aliases=["aghs", "ags", "aghanims", "scepter", "shard"])
    async def aghanim(self, ctx, *, name = None):
        """Melihat aghanim upgrade untuk hero atau ability DOTA 2"""
        print("Command aghanim dialihkan ke MangoByte")
        
    @commands.command()
    async def blog(self, ctx):
        """Berita terbaru seputar DOTA 2"""
        print("Command aghanim dialihkan ke MangoByte")

    @commands.command(aliases=["fuse", "fuze", "fuzeheroes"])
    async def fuseheroes(self, ctx, *, heroes = None):
        """Lihatlah apa yang terjadi jika kamu menggabungkan 2 hero DOTA 2
        Jika kamu tidak memasukan hero, aku akan memberikan secara random

        **Contoh:**
        acx fuseheroes axe chen"""
        print("Command fuseheros dialihkan ke MangoByte")

    @commands.command()
    async def laning(self, ctx, match_id = None):
        """Membuat lanning dalam bentuk gif

        Jika kamu tidak memasukan match_id, aku akan mengambil data lastmatch dari akun mu yang telah terhubung dengan Acinonyx"""
        print("Command laning dialihkan ke MangoByte")

    @commands.command()
    async def blog(self,ctx):
        """Berita terbaru seputar DOTA 2"""
        print("Command laning dialihkan ke MangoByte")

    @commands.command()
    async def lastmatch(self, ctx, *, matchfilter  = None):
        """Mendapatkan informasi pertandingan terakhir player DOTA 2"""
        print("Command lastmatch dialihkan ke MangoByte")

    @commands.command(aliases=["whois"])
    async def profile(self, ctx, player  = None):
        """Menampilkan informasi profile player DOTA 2.
        Jika kamu tidak mengisi `DotaPlayer` aku hanya akan mengambil id steam milik mu yang telah di set.
        
        `DotaPlayer` hanya dapat di isi dengan nomor id steam32 atau steam64, atau @mention member jika dia sudah melakukan set id steam.
        """
        print("Command profile dialihkan ke MangoByte")

    @commands.command()
    async def firstmatch(self, ctx, *, matchfilter = None):
        """Mendapatkan informasi pertandingan pertama kalinya pada saat player bermain DOTA 2"""
        print("Command firstmatch dialihkan ke MangoByte")

    @commands.command()
    async def match(self, ctx, match_id : int):
        """Melihat ringkasan pertandingan dota dengan id yang diberikan"""
        print("Command match dialihkan ke MangoByte")

    @commands.command()
    async def matchstory(self, ctx, match_id : int, perspective=None):
        """Mengetahui alur cerita dari pertandingan

        Alur cerita ditentukan dari perspective sebegai:
        • radiant
        • dire
        """
        print("Command matchstory dialihkan ke MangoByte")

    @commands.command()
    async def skillbuild(self, ctx, match_id : int):
        """Melihat ability upgrade dalam pertandingan"""
        print("Command skillbuild dialihkan ke MangoByte")

    @commands.command(aliases=["recentmatches", "recent"])
    async def matches(self, ctx, *, matchfilter = None):
        """Menampilkan list pertandinga  DOTA 2 mu dalam bentuk gambar
        Tanggal/waktu berdasarkan server tempat permainan dimainkan, dan mungkin tidak akan sesuai dengan zona waktu mu

        **Catatan:**
        Kamu dapat menampilkan pertandingan mu hingga 100.
        jika kamu tidak memasukan `matchfilter` aku akan memberikan 10 list pertandingan

        **Contoh :**
        acx matches 20
        acx matches @member mid witch doctor ranked
        acx matches natures prophet
        acx matches @member riki"""
        print("Command matches dialihkan ke MangoByte")

    @commands.command()
    async def matchids(self, ctx, *, matchfilter = None):
        """Mendapatkan list pertandingan DOTA 2
        Aku akan memberikan 10 match id secara default, jika kamu tidak mengisi matchfilter

        **Contoh:**
        acx matchids 20
        acx matchids @member mid witch doctor ranked
        acx matchids natures prophet
        acx matchids @member riki"""
        print("Command matchids dialihkan ke MangoByte")

    @commands.command()
    async def aboutdotabase(self, ctx):
        """Tentang DotaBase.py dalam kategori ini"""
        msg  = "Semua command ini dalam kategori *`DotaBase.py`*\n"
        msg += "*`{}help DotaBase`*\n".format(ctx.prefix)
        msg += "Merupakan karya original dari [MangoByte](https://github.com/mdiller/MangoByte/).\n\n"
        msg += "Saya (owner/pemilik) dari bot ini hanya melakukan re-work karya dari [MangoByte](https://github.com/mdiller/MangoByte/)\n"
        msg += "agar dapat berfungsi dengan baik dalam bot Acinonyx dan mengubah beberapa bahasa dari inggris ke indonesia.\n\n"
        msg += "Invite bot MangoByte link dibawah ini.\n"
        msg += "**[MangoByte Official Bot](https://discord.com/oauth2/authorize?permissions=314432&scope=bot&client_id=213476188037971968)**"
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_author(name = "DotaBase DISCLAIMER")
        em.set_footer(text = "{}".format(ctx.author), icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)