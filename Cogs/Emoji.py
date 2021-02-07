import discord, os
from discord.ext import commands
from Cogs import GetImage, Utils

def setup(bot):
    bot.add_cog(Emoji(bot))

class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.max_emojis = 10
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")

    def _get_emoji_url(self, emoji):
        if len(emoji) < 3:
            # Emoji is likely a built-in like :)
            h = "-".join([hex(ord(x)).lower()[2:] for x in emoji])
            return ("https://github.com/twitter/twemoji/raw/master/assets/72x72/{}.png".format(h),h)
        # Must be a custom emoji
        emojiparts = emoji.replace("<","").replace(">","").split(":") if emoji else []
        if not len(emojiparts) == 3: return None
        # Build a custom emoji object
        emoji_obj = discord.PartialEmoji(animated=len(emojiparts[0]) > 0, name=emojiparts[1], id=emojiparts[2])
        # Return the url
        return (emoji_obj.url,emoji_obj.name)

    def _get_emoji_mention(self, emoji):
        return "<{}:{}:{}>".format("a" if emoji.animated else "",emoji.name,emoji.id)

    @commands.command()
    async def addemoji(self, ctx, *, emoji = None, name = None):
        '''Menambahkan emoji (bot-admin only, maksimal 10 dalam 1 command)
        Dengan format berupa:
        • Attachment Gambar (Upload gambar)
        • Link URL
        • Atau emoji dari server lain (lebih mudah untuk pengguna nitro)'''
        if not await Utils.is_bot_admin_reply(ctx): return
        if not len(ctx.message.attachments) and emoji == name == None:
            em = discord.Embed(color = 0XFF8C00, description =  "> Upload emoji gak usak pake ribet\n> \n"
                                                                "> **Panduan pengunaan**\n"
                                                                "> `{}addemoji [emoji server lain, url, attachment] [name]`"
                                                               .format(ctx.prefix))
            em.set_author(name = "Help command", url = "https://acinonyxesports.com/", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = f"Saat mengetik command, tanda [] tidak usah digunakan.\nRequest By : {ctx.author.name}", icon_url = f"{ctx.author.avatar_url}")
            return await ctx.send(embed = em)
        # Let's find out if we have an attachment, emoji, or a url
        # Check attachments first - as they'll have priority
        if len(ctx.message.attachments):
            name = emoji
            emoji = " ".join([x.url for x in ctx.message.attachments])
            if name: # Add the name separated by a space
                emoji += " "+name
        # Now we split the emoji string, and walk it, looking for urls, emojis, and names
        emojis_to_add = []
        last_name = []
        for x in emoji.split():
            # Check for a url
            urls = Utils.get_urls(x)
            if len(urls):
                url = (urls[0], os.path.basename(urls[0]).split(".")[0])
            else:
                # Check for an emoji
                url = self._get_emoji_url(x)
                if not url:
                    # Gotta be a part of the name - add it
                    last_name.append(x)
                    continue
            if len(emojis_to_add) and last_name:
                # Update the previous name if need be
                emojis_to_add[-1][1] = "".join([z for z in "_".join(last_name) if z.isalnum() or z == "_"])
            # We have a valid url or emoji here - let's make sure it's unique
            if not url[0] in [x[0] for x in emojis_to_add]:
                emojis_to_add.append([url[0],url[1]])
            # Reset last_name
            last_name = []
        if len(emojis_to_add) and last_name:
            # Update the final name if need be
            emojis_to_add[-1][1] = "".join([z for z in "_".join(last_name) if z.isalnum() or z == "_"])
        em = discord.Embed(color = 0XFF8C00, description = "> Upload emoji gak usak pake ribet\n> \n"
                                                           "> **Panduan pengunaan**\n"
                                                           "> `{}addemoji [emoji server lain, url, attachment] [nama]`"
                                                           .format(ctx.prefix))
        em.set_author(name = "Help command", url = "https://acinonyxesports.com/", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
        em.set_footer(text = f"Saat mengetik command, tanda [] tidak usah digunakan.\nRequest By : {ctx.author.name}", icon_url = f"{ctx.author.avatar_url}")
        if not emojis_to_add: return await ctx.send(embed = em)
        # Now we have a list of emojis and names
        added_emojis = []
        allowed = len(emojis_to_add) if len(emojis_to_add)<=self.max_emojis else self.max_emojis
        omitted = " ({} gambar dihilangkan, karena melebihi batas maksimal {})".format(len(emojis_to_add)-self.max_emojis,self.max_emojis) if len(emojis_to_add)>self.max_emojis else ""
        message = await ctx.send("Menambahkan {} emoji{}{}...".format(
            allowed,
            "" if allowed==1 else "",
            omitted))
        for emoji_to_add in emojis_to_add[:self.max_emojis]:
            # Let's try to download it
            emoji,e_name = emoji_to_add # Expand into the parts
            f = await GetImage.download(emoji)
            if not f: continue
            # Open the image file
            with open(f,"rb") as e:
                image = e.read()
            # Clean up
            GetImage.remove(f)
            if not e_name.replace("_",""): continue
            # Create the emoji and save it
            try: new_emoji = await ctx.guild.create_custom_emoji(name=e_name,image=image,roles=None,reason="Added by {}#{}".format(ctx.author.name,ctx.author.discriminator))
            except: continue
            added_emojis.append(new_emoji)
        msg = "Membuat {} dari {} emoji{}{}.".format(
            len(added_emojis),
            allowed,"" if allowed==1 else "",
            omitted
            )
        if len(added_emojis):
            msg += "\n\n"
            emoji_text = ["{} - `:{}:`".format(self._get_emoji_mention(x),x.name) for x in added_emojis]
            msg += "\n".join(emoji_text)
        em = discord.Embed(color = 0XFF8C00, description =  msg)
        em.set_author(name = "Berhasil menambahkan emoji", url = "https://acinonyxesports.com/", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
        em.set_footer(text = f"Request By : {ctx.author.name}", icon_url = f"{ctx.author.avatar_url}")
        await message.edit(embed=em)

    @commands.command()
    async def emoji(self, ctx, emoji = None):
        '''Menampilkan emoji, tapi dengan ukuran yang lebih BESAAAAAAR!'''
        if emoji is None:
            em = discord.Embed(color = 0XFF8C00, description =  "> Menampilkan Emoji, Dengan ukuran lebih BESAAAAAARRR!1!11!\n> \n"
                                                                "> **Panduan pengunaan**\n"
                                                                "> `{}emoji [emoji]`"
                                                                .format(ctx.prefix))
            em.set_author(name = "Help command", url = "https://acinonyxesports.com/", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
            em.set_footer(text = f"Saat mengetik command, tanda [] tidak usah digunakan.\nRequest By : {ctx.author.name}", icon_url = f"{ctx.author.avatar_url}")
            await ctx.send(embed = em)
            return
        # Get the emoji
        emoji_url = self._get_emoji_url(emoji)
        em = discord.Embed(color = 0XFF8C00, description =  "> Menampilkan Emoji, Dengan ukuran lebih BESAAAAAARRR!1!11!\n> \n"
                                                            "> **Panduan pengunaan**\n"
                                                           f"> `{ctx.prefix}emoji [emoji]`")
        em.set_author(name = "Help command", url = "https://acinonyxesports.com/", icon_url = "https://cdn.discordapp.com/attachments/518118753226063887/725569194304733435/photo.jpg")
        em.set_footer(text = f"Saat mengetik command, tanda [] tidak usah digunakan.\nRequest By : {ctx.author.name}", icon_url = f"{ctx.author.avatar_url}")
        if not emoji_url: return await ctx.send(embed = em)
        f = await GetImage.download(emoji_url[0])
        if not f: return await ctx.send("┐(￣ヘ￣;)┌\nAku tidak dapat menemukan emoji itu")
        await ctx.send(file=discord.File(f))
        # Clean up
        GetImage.remove(f)
