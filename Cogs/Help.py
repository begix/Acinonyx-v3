import asyncio
import discord
import random
import math
import os
from   datetime import datetime
from   operator import itemgetter
from   discord.ext import commands
from   Cogs import ReadableTime
from   Cogs import Nullify
from   Cogs import DisplayName
from   Cogs import Message
from   Cogs import FuzzySearch


HelpMsg = """**Welcome & Goodbye Message**
`setwelcome`,`setgoodbye`,`setwelcomechannel`,`testgoodbye`,`testwelcome`

**Moderasi Server**
`addadmin`, `removeadmin`, `lock`, `ban`, `kick`, `ignore`, `listen`, `removeinvitelinks`, `log`, `setrules`, `joinpm`, `clean`, `logenable`, `logdisable`, `logging`, `setlogchannel`, `adminallow`, `badminallow`, `disable`, `enable`, `disableall`, `enableall`, `listdisabled`, `disablereact`, `addemoji`, `ignoredeath`, `kill`, `resurrect`, `setkillrole`, `tableflip`, `addfilter`, `clearfilter`, `dumpfilter`, `listfilter`, `remfilter`, `createmuterole`, `syncmuterole`, `desyncmuterole`

**Action**
`drink`, `eat`, `pet`, `spook`,`poke`,`stardew`

**OSU!**
`setosu`, `std`, `taiko`, `ctb`, `mania`, `rstd`, `rtaiko`, `rctb`, `rmania`

**DOTA 2**
`abilities`, `ability`, `hero`, `item`, `lore`, `leveledstats`, `talents`

**Comic**
`calvin`, `cyanide`, `dilbert`, `gmg`, `randcalvin`, `randcyanide`, `randgmg`, `randilbert`, `randxkcd`, `xkcd`

**Fun**
`calc`, `ascii`, `roll`, `eightball`, `color`, `meme`, `memetemps`, `zalgo`, `morse`, `unmorse`

**Image Filter**
`blue`, `blur`, `blurple`, `brightness`, `green`, `greycsale`, `invert`, `pixelate`, `red`, `sepia`, `threshold`

**Chatbot**
`chat`, `setchatchannel`


**Reddit image**
`reddit`

**Utils**
`rolecount`, `whohas`, `emptyroles`, `roles`, `avi`, `messages`, `allmessages`, `firstjoin`, `users`, `serverinfo`, `botinfo`, `cloc`, `ping`, `servers`, `stats`, `invite`, `donate`

Masih ada lebih dari 100+ command di bot ini
Kamu bisa melihat command lainnya **[disini](https://dark-kazoeru.gitbook.io/acinonyx/commands/help-command)**
[Website](https://acinonyxesports.com) | [Support Server](https://discord.gg/vMcMe8f) | [Acinonyx full docs](https://dark-kazoeru.gitbook.io/acinonyx) | [Donasi](https://saweria.co/NvStar)"""


def setup(bot):
    # Add the cog
    bot.remove_command("help")
    bot.add_cog(Help(bot))

# This is the Help module. It replaces the built-in help command

class Help(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")
        
    def _get_prefix(self, ctx):
        # Helper method to get the simplified prefix
        # Setup a clean prefix
        if ctx.guild:
            bot_member = ctx.guild.get_member(self.bot.user.id)
        else:
            bot_member = ctx.bot.user
        # Replace name and nickname mentions
        return ctx.prefix.replace(bot_member.mention, '@' + DisplayName.name(bot_member))

    def _is_submodule(self, parent, child):
        return parent == child or child.startswith(parent + ".")

    def _get_help(self, command, max_len = 0):
        # A helper method to return the command help - or a placeholder if none
        if max_len == 0:
            # Get the whole thing
            if command.help == None:
                return "Help not available..."
            else:
                return command.help
        else:
            if command.help == None:
                c_help = "Help not available..."
            else:
                c_help = command.help.split("\n")[0]
            return (c_help[:max_len-3]+"...") if len(c_help) > max_len else c_help

    async def _get_info(self, ctx, com = None):
        # Helper method to return a list of embed content
        # or None if no results

        prefix = self._get_prefix(ctx)

        # Setup the footer
        footer = "\nKetik `{}help command` untuk informasi lebih lanjut. \n".format(prefix)
        #footer += "You can also type `{}help category` for more info on a category.".format(prefix)

        # Get settings - and check them if they exist
        disabled_list = None
        settings = self.bot.get_cog("Settings")
        if settings and ctx.guild:
            disabled_list = settings.getServerStat(ctx.guild, "DisabledCommands")
        if disabled_list == None:
            disabled_list = []

        if com == None:
            # No command or cog - let's send the coglist
            embed_list = { "title" : "Help command", "fields" : []}
            DescMsg = ">>> <:9032_Senko_happy_nosies:803886640564011019> Halo nama ku Acinonyx\njangan ragu untuk menggunakan ku dalam server mu\nKetik *`{}help [command]`* untuk informasi lebih lanjut".format(ctx.prefix)
            embed_list["description"] = DescMsg
            
            valueMsg = "*```\naddadmin, removeadmin, lock, ban, kick, ignore, listen, removeinvitelinks, log, setrules, joinpm, clean, logenable, logdisable, logging, setlogchannel, adminallow, badminallow, disable, enable, disableall, enableall, listdisabled, disablereact, addemoji, ignoredeath, kill, resurrect, setkillrole, tableflip, addfilter, clearfilter, dumpfilter, listfilter, remfilter, createmuterole, syncmuterole, desyncmuterole\n```*"
            embed_list["fields"].append({ "name" : "<:3869501:803893026313338912> Moderasi server", "value" : valueMsg, "inline" : False })
            
            valueMsg = "*```\nsetosu, std, taiko, ctb, mania, rstd, rtaiko, rctb, rmania\n```*"
            embed_list["fields"].append({ "name" : "<:4271_osu:803893978390462474> Osu!", "value" : valueMsg})
            
            valueMsg = "*```\nabilities, ability, hero, item, lore, leveledstats, talents, lore, courage, herotable, neutralitems, aghanim, blog, fusehero, laning, firstmatch, lastmatch, profile, matchstory, matches, matchids, skillbuild, userconfig, parse, aboutdotabase\n```*"
            embed_list["fields"].append({ "name" : "<:2994_dota2:803907077541068840> DOTA 2", "value" : valueMsg})

            valueMsg = "*```randcalvin, randcyanide, randgmg, randilbert, randxkcd, calvin, cyanide, gmg, dilbert, xkcd, randcalvin```*"
            embed_list["fields"].append({ "name" : "<:comic:804319701437906964> Comic", "value" : valueMsg})

            valueMsg = "*```\ncalc, ascii, roll, eightball, color, meme, memetemps, zalgo, morse, unmorse, emoji, weather, tconvert, forecast, wiki,  blue, blur, blurple, brightness, green, greycsale, invert, pixelate, red, sepia, threshold\n```*"
            embed_list["fields"].append({ "name" : "<:fun:803918712440225793> Fun", "value" : valueMsg})

            valueMsg = "*```\nabandoned, aww, battlestation, beeple, cablefail, carmod, dankmeme, dragon, earthporn, macsetup, meirl, pun, randomcat, randomdog, reddit, ruser, shittybattlestation, software, starterpack, techsupport, wallpaper\n```*"
            embed_list["fields"].append({ "name" : "<:reddit:803910953938583582> Reddit", "value" : valueMsg})
            
            valueMsg = "*```\nrolecount, whohas, emptyroles, roles, avi, messages, allmessages, users, serverinfo, botinfo, cloc, ping, servers, stats, settz, listtz, lastonline, online, invite, joinpos, time, tz, uptime, donate\n```*"
            embed_list["fields"].append({ "name" : "<:utils:803919381833711616> Utils", "value" : valueMsg})

            valueMsg =  ">>> Acinonyx masih punya lebih dari 200 command loh.\n"
            valueMsg += "Klik **[DISINI](https://dark-kazoeru.gitbook.io/acinonyx/commands/help-command)** yaa.\n\n"
            valueMsg += "**Acinonyx Official Website**\n"
            valueMsg += "[Website](https://acinonyxesports.com) | [Support Server](https://discord.gg/vMcMe8f) | [Acinonyx full docs](https://dark-kazoeru.gitbook.io/acinonyx) | [Donasi](https://saweria.co/NvStar) | [Invite aku](https://discord.com/oauth2/authorize?client_id=725197780162838609&scope=bot&permissions=8)"
            embed_list["fields"].append({ "name" : "<:website:803921231266578432> Other command & Website", "value" : valueMsg})
            # embed_list = { "title" : "Current Categories", "fields" : [] }
            # command_list = []
            # for cog in sorted(self.bot.cogs):
            #   if not len(self.bot.get_cog(cog).get_commands()):
            #       # Skip empty cogs
            #       continue
            #   # Make sure there are non-hidden commands here
            #   visible = []
            #   disabled = 0
            #   for command in self.bot.get_cog(cog).get_commands():
            #       if not command.hidden:
            #           visible.append(command)
            #       if command.name in disabled_list:
            #           disabled += 1
            #   if not len(visible):
            #       continue
            #   # Add the name of each cog in the list
            #   if disabled == 0:
            #       new_dict = { "name" : cog }
            #   elif disabled == len(visible):
            #       new_dict = { "name" : "~~" + cog + "~~ (Disabled)" }
            #   else:
            #       new_dict = { "name" : cog + " ({} Disabled)".format(disabled) }
            #   if len(visible) == 1:
            #       new_dict["value"] = "`└─ 1 command`"
            #   else:
            #       new_dict["value"] = "`└─ {:,} commands`".format(len(visible))
            #   new_dict["inline"] = True
            #   embed_list["fields"].append(new_dict)
            return embed_list
        else:
            for cog in sorted(self.bot.cogs):
                if not cog == com:
                    continue
                # Found the cog - let's build our text
                cog_commands = sorted(self.bot.get_cog(cog).get_commands(), key=lambda x:x.name)
                # Get the extension
                the_cog = self.bot.get_cog(cog)
                embed_list = None
                for e in self.bot.extensions:
                    b_ext = self.bot.extensions.get(e)
                    if self._is_submodule(b_ext.__name__, the_cog.__module__):
                        # It's a submodule
                        embed_list = {"title" : "{} Cog - {}.py Extension". format(cog, e[5:]), "fields" : [] }
                        break
                if not embed_list:
                    embed_list = {"title" : cog, "fields" : [] }
                for command in cog_commands:
                    # Make sure there are non-hidden commands here
                    if command.hidden:
                        continue
                    command_help = self._get_help(command, 80)
                    if command.name in disabled_list:
                        name = "~~" + prefix + command.name + " " + command.signature + "~~ (Disabled)"
                    else:
                        name = prefix + command.name + " " + command.signature
                    embed_list["fields"].append({ "name" : name, "value" : "`└─ " + command_help + "`", "inline" : False })
                # If all commands are hidden - pretend it doesn't exist
                if not len(embed_list["fields"]):
                    return None
                return embed_list
            # If we're here, we didn't find the cog - check for the command
            for cog in self.bot.cogs:
                cog_commands = sorted(self.bot.get_cog(cog).get_commands(), key=lambda x:x.name)
                for command in cog_commands:
                    if not command.name == com:
                        continue
                    # Get the extension
                    the_cog = self.bot.get_cog(cog)
                    embed_list = None
                    for e in self.bot.extensions:
                        b_ext = self.bot.extensions.get(e)
                        if self._is_submodule(b_ext.__name__, the_cog.__module__):
                            # It's a submodule
                            embed_list = {"title" : "{} Cog - {}.py Extension".format(cog, e[5:]), "fields" : [] }
                            break
                    if not embed_list:
                        embed_list = { "title" : cog }
                    if command.name in disabled_list:
                        embed_list["description"] = "~~**{}**~~ (Disabled)\n```\n{}```".format(prefix + command.name + " " + command.signature, command.help)
                    else:
                        embed_list["description"] = "**{}**\n```\n{}```".format(prefix + command.name + " " + command.signature, command.help) 
                    return embed_list
        # At this point - we got nothing...
        return None

    async def _send_embed(self, ctx, embed, pm = False):
        # Helper method to send embeds to their proper location
        if pm == True and not ctx.channel == ctx.author.dm_channel:
            # More than 2 pages, try to dm
            try:
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction("📬")
            except discord.Forbidden:
                await ctx.send(embed=embed)
            return
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def dumphelp(self, ctx, tab_indent_count = None):
        """Backup semua help list dalam bentuk format file text.txt"""
        try:
            tab_indent_count = int(tab_indent_count)
        except:
            tab_indent_count = None
        if tab_indent_count == None or tab_indent_count < 0:
            tab_indent_count = 1

        timeStamp = datetime.today().strftime("%Y-%m-%d %H.%M")
        serverFile = 'HelpList-{}.txt'.format(timeStamp)
        message = await ctx.send('Saving help list to *{}*...'.format(serverFile))
        msg = ''
        prefix = self._get_prefix(ctx)
        
        # Get and format the help
        for cog in sorted(self.bot.cogs):
            cog_commands = sorted(self.bot.get_cog(cog).get_commands(), key=lambda x:x.name)
            cog_string = ""
            # Get the extension
            the_cog = self.bot.get_cog(cog)
            # Make sure there are non-hidden commands here
            visible = []
            for command in self.bot.get_cog(cog).get_commands():
                if not command.hidden:
                    visible.append(command)
            if not len(visible):
                # All hidden - skip
                continue
            cog_count = "1 command" if len(visible) == 1 else "{} command".format(len(visible))
            for e in self.bot.extensions:
                b_ext = self.bot.extensions.get(e)
                if self._is_submodule(b_ext.__name__, the_cog.__module__):
                    # It's a submodule
                    cog_string += "{}{} Cog ({}) - {}.py Extension:\n".format(
                        "   "*tab_indent_count,
                        cog,
                        cog_count,
                        e[5:]
                    )
                    break
            if cog_string == "":
                cog_string += "{}{} Cog ({}):\n".format(
                    "   "*tab_indent_count,
                    cog,
                    cog_count
                )
            for command in cog_commands:
                cog_string += "{}  {}\n".format("   "*tab_indent_count, prefix + command.name + " " + command.signature)
                cog_string += "{}  {}└─ {}\n".format(
                    "   "*tab_indent_count,
                    " "*len(prefix),
                    self._get_help(command, 80)
                )
            cog_string += "\n"
            msg += cog_string
        
        # Encode to binary
        # Trim the last 2 newlines
        msg = msg[:-2].encode("utf-8")
        with open(serverFile, "wb") as myfile:
            myfile.write(msg)

        await message.edit(content='Uploading *{}*...'.format(serverFile))
        await ctx.send(file=discord.File(serverFile))
        await message.edit(content='Uploaded *{}!*'.format(serverFile))
        os.remove(serverFile)

    @commands.command(pass_context=True)
    async def dumpmarkdown(self, ctx):
        """Backup semua help list dalam bentuk file format markdown.md"""
        tab_indent_count = 1

        timeStamp = datetime.today().strftime("%Y-%m-%d %H.%M")
        serverFile = 'HelpMarkdown-{}.md'.format(timeStamp)
        message = await ctx.send('Saving help list to *{}*...'.format(serverFile))
        prefix = self._get_prefix(ctx)
        
        #msg = "\n".join(["* [{}](#{})".format(x,x.lower()) for x in sorted(self.bot.cogs)])
        #msg += "\n\n"
        cog_list = []
        msg = ""
        # Get and format the help
        for cog in sorted(self.bot.cogs):
            cog_commands = sorted(self.bot.get_cog(cog).get_commands(), key=lambda x:x.name)
            cog_string = ""
            # Get the extension
            the_cog = self.bot.get_cog(cog)
            # Make sure there are non-hidden commands here
            visible = []
            for command in self.bot.get_cog(cog).get_commands():
                if not command.hidden:
                    visible.append(command)
            if not len(visible):
                # All hidden - skip
                continue
            cog_list.append(cog)
            cog_count = "1 command" if len(visible) == 1 else "{} command".format(len(visible))
            for e in self.bot.extensions:
                b_ext = self.bot.extensions.get(e)
                if self._is_submodule(b_ext.__name__, the_cog.__module__):
                    # It's a submodule
                    cog_string += "## {}\n".format(cog)
                    cog_string += "####{}{} Cog ({}) - {}.py Extension:\n".format(
                        "   "*tab_indent_count,
                        cog,
                        cog_count,
                        e[5:]
                    )
                    break
            if cog_string == "":
                cog_string += "## {}\n".format(cog)
                cog_string += "####{}{} Cog ({}):\n".format(
                    "   "*tab_indent_count,
                    cog,
                    cog_count
                )
            for command in cog_commands:
                cog_string += "{}  {}\n".format("   "*tab_indent_count, prefix + command.name + " " + command.signature)
                cog_string += "{}  {}└─ {}\n".format(
                    "   "*tab_indent_count,
                    " "*len(prefix),
                    self._get_help(command, 80)
                )
            cog_string += "\n"
            msg += cog_string
        msg = ", ".join(["[{}](#{})".format(x,x.lower()) for x in sorted(cog_list)])+"\n\n"+msg
        # Encode to binary
        # Trim the last 2 newlines
        msg = msg[:-2].encode("utf-8")
        with open(serverFile, "wb") as myfile:
            myfile.write(msg)

        await message.edit(content='Uploading *{}*...'.format(serverFile))
        await ctx.send(file=discord.File(serverFile))
        await message.edit(content='Uploaded *{}!*'.format(serverFile))
        os.remove(serverFile)

    @commands.command(pass_context=True)
    async def help(self, ctx, *, command = None):
        """Melihat list help.
        You can pass a command or cog to this to get more info (case-sensitive)."""
        
        result = await self._get_info(ctx, command)

        if result == None:
            # Get a list of all commands and modules and server up the 3 closest
            cog_name_list = []
            com_name_list = []
            
            for cog in self.bot.cogs:
                if not cog in cog_name_list:
                    if not len(self.bot.get_cog(cog).get_commands()):
                        # Skip empty cogs
                        continue
                cog_commands = self.bot.get_cog(cog).get_commands()
                hid = True
                for comm in cog_commands:
                    if comm.hidden:
                        continue
                    hid = False
                    if not comm.name in com_name_list:
                        com_name_list.append(comm.name)
                if not hid:
                    cog_name_list.append(cog)
            
            # Get cog list:
            cog_match = FuzzySearch.search(command, cog_name_list)
            com_match = FuzzySearch.search(command, com_name_list)

            # Build the embed
            m = Message.Embed(force_pm=True,pm_after=25)
            if type(ctx.author) is discord.Member:
                m.color = 0XFF8C00
            m.title = "Tidak ada command \"{}\" yang ditemukan".format(Nullify.clean(command))
            if len(cog_match):
                cog_mess = ""
                for pot in cog_match:
                    cog_mess += '└─ {}\n'.format(pot['Item'].replace('`', '\\`'))
                m.add_field(name="Mungkin Kategori ini yang kamu maksud:", value=cog_mess)
            if len(com_match):
                com_mess = ""
                for pot in com_match:
                    com_mess += '└─ {}\n'.format(pot['Item'].replace('`', '\\`'))
                m.add_field(name="Mungkin Command ini yang kamu maksud:", value=com_mess)
            m.footer = { "text" : "Ingat Kategori dan command peka terhadap huruf BESAR/kecil.", "icon_url" : self.bot.user.avatar_url }
            await m.send(ctx)
            return
        m = Message.Embed(**result)
        m.force_pm = True
        m.pm_after = 25
        # Build the embed
        if type(ctx.author) is discord.Member:
            m.color = 0XFF8C00
        m.footer = self.bot.description + "\nKetik \"{}help command\" untuk informasi lebih lanjut. \n".format(self._get_prefix(ctx))
        await m.send(ctx)
