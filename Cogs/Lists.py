import asyncio, discord, time
from   discord.ext import commands
from   Cogs import Utils, ReadableTime, DisplayName, FuzzySearch, Message, PickList

def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(Lists(bot, settings))

# This is the lists module.

class Lists(commands.Cog):

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot, settings):
        self.bot = bot
        global Utils, DisplayName
        Utils = self.bot.get_cog("Utils")
        DisplayName = self.bot.get_cog("DisplayName")
        self.settings = settings
        self.alt_lists = [ { 
            "command" : "hack",
            "list" : "Hacks"
        }, { 
            "command" : "link",
            "list" : "Links"
        }, { 
            "command" : "tag",
            "list" : "Tags"
        } ]
        self.presets = {
            "Link": {
                "l_list": "Links",
                "l_name": "Link",
                "l_key" : "URL",
                "l_role": "RequiredLinkRole",
            },
            "Hack": {
                "l_list": "Hacks",
                "l_name": "Hack",
                "l_key" : "Hack",
                "l_role": "RequiredHackRole",
            },
            "Tag": {
                "l_list": "Tags",
                "l_name": "Tag",
                "l_key" : "URL",
                "l_role": "RequiredTagRole",
            }
        }
        
        
    '''async def onjoin(self, member, server):
        # Resolve our status based on the most occurances of UTCOffset
        newVal = self.settings.getGlobalUserStat(member, "Parts", server)
        self.settings.setUserStat(member, server, "Parts", newVal)'''

    ###                        ###
    ## Generic Accessor Methods ##
    ###                        ###

    def _has_privs(self,ctx,l_role="RequiredLinkRole"):
        if not Utils.is_bot_admin(ctx):
            required_role = self.settings.getServerStat(ctx.guild, l_role, "")
            if required_role == "" or not ctx.guild.get_role(int(required_role)) in ctx.author.roles:
                return False
        return True

    async def _get_item(self,ctx,name,l_role="RequiredLinkRole",l_list="Links",l_name="Link",l_key="URL",raw=False):
        # Helper function to pull items from lists
        if not name:
            em = discord.Embed(color = 0XFF8C00, description = '**Panduan**\n'
                                                               '`{}{}[[name]] "[[[name]] name]"`'
                                                               .format(ctx.prefix,"raw" if raw else "").replace("[[name]]",l_name.lower()))
            em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                          icon_url = "{}".format(ctx.author.avatar_url))
            return await ctx.send(embed = em)
        itemList = self.settings.getServerStat(ctx.guild, l_list)
        # Check other lists
        other_commands = []
        other_names    = []
        for i in self.alt_lists:
            if i["list"] == l_list:
                # Our list - skip
                continue
            check_list = self.settings.getServerStat(ctx.guild, i["list"])
            if any(x["Name"].lower() == name.lower() for x in check_list):
                # Add the list
                other_commands.append(i)
                other_names.append(Utils.suppressed(ctx,"{}{} {}".format(ctx.prefix,i["command"],name)))
                
        if not itemList or itemList == []:
            no_items = 'No [[name]]s in list!  You can add some with the `{}add[[name]] "[[[name]] name]" [[[key]]]` command!'.format(ctx.prefix).replace("[[name]]",l_name.lower()).replace("[[key]]",l_key.lower())
            if raw or not len(other_commands):
                # No other matches
                return await ctx.send(no_items)
            msg = no_items + "\n\nMaybe you meant:"
            index, message = await PickList.Picker(
                title=msg,
                list=other_names,
                ctx=ctx
            ).pick()
            # Check if we errored/cancelled
            if index < 0:
                return await message.edit(content=no_items)
            # Got something
            await message.edit(content="`{}`".format(other_names[index]))
            # Invoke
            return await ctx.invoke(self.bot.all_commands.get(other_commands[index]["command"]), name=name)

        for item in itemList:
            if item['Name'].lower() == name.lower():
                msg = '**{}:**\n{}'.format(item['Name'], discord.utils.escape_markdown(item[l_key]) if raw else item[l_key])
                return await ctx.send(Utils.suppressed(ctx,msg))
                
        not_found = Utils.suppressed(ctx,'`{}` not found in {} list!'.format(name.replace("`", "").replace("\\",""),l_name.lower()))
        # No matches - let's fuzzy search
        potentialList = FuzzySearch.search(name, itemList, 'Name')
        if len(potentialList):
            # Setup and display the picker
            msg = not_found + '\n\nSelect one of the following close matches:'
            p_list = [x["Item"]["Name"] for x in potentialList]
            p_list.extend(other_names)
            index, message = await PickList.Picker(
                title=msg,
                list=p_list,
                ctx=ctx
            ).pick()
            # Check if we errored/cancelled
            if index < 0:
                return await message.edit(content=not_found)
            # Check if we have another command
            if index >= len(potentialList):
                # We're into our other list
                await message.edit(content="`{}`".format(other_names[index - len(potentialList)]))
                # Invoke
                return await ctx.invoke(self.bot.all_commands.get(other_commands[index - len(potentialList)]["command"]), name=name)
            # Display the item
            for item in itemList:
                if item["Name"] == potentialList[index]["Item"]["Name"]:
                    msg = '**{}:**\n{}'.format(item['Name'], discord.utils.escape_markdown(item[l_key]) if raw else item[l_key])
                    return await message.edit(content=Utils.suppressed(ctx,msg))
            return await message.edit(content="{} `{}` no longer exists!".format(
                l_name,
                potentialList[index]["Item"]["Name"].replace("`", "").replace("\\",""))
            )
        # Here we have no potentials
        return await ctx.send(not_found)

    async def _add_item(self,ctx,name,value,l_role="RequiredLinkRole",l_list="Links",l_name="Link",l_key="URL"):
        # Check if we're admin/bot admin first - then check for a required role
        if not self._has_privs(ctx,l_role): return await ctx.send("You do not have sufficient privileges to access this command.")
        # Remove tabs, newlines, and carriage returns and strip leading/trailing spaces from the name
        name = None if name == None else name.replace("\n"," ").replace("\r","").replace("\t"," ").strip()
        # Passed role requirements!
        if name == None or value == None:
            msg = 'Usage: `{}add[[name]] "[[[name]] name]" [[[key]]]`'.format(ctx.prefix).replace("[[name]]",l_name.lower()).replace("[[key]]",l_key.lower())
            return await ctx.send(msg)
        safe_name = name.replace("`", "").replace("\\","")
        itemList = self.settings.getServerStat(ctx.guild, l_list)
        if not itemList:
            itemList = []
        currentTime = int(time.time())
        item = next((x for x in itemList if x["Name"].lower() == name.lower()),None)
        if item:
            safe_name = item["Name"].replace("`", "").replace("\\","")
            msg = Utils.suppressed(ctx,'`{}` updated!'.format(safe_name))
            item[l_key]       = value
            item['UpdatedBy'] = DisplayName.name(ctx.author)
            item['UpdatedID'] = ctx.author.id
            item['Updated']   = currentTime
        else:
            itemList.append({"Name" : name, l_key : value, "CreatedBy" : DisplayName.name(ctx.author), "CreatedID": ctx.author.id, "Created" : currentTime})
            msg = Utils.suppressed(ctx,'`{}` added to {} list!'.format(safe_name,l_name.lower()))
        self.settings.setServerStat(ctx.guild, l_list, itemList)
        return await ctx.send(Utils.suppressed(ctx,msg))

    async def _remove_item(self,ctx,name,l_role="RequiredLinkRole",l_list="Links",l_name="Link",l_key="URL"):
        if not self._has_privs(ctx,l_role): return await ctx.send("You do not have sufficient privileges to access this command.")
        if name == None:
            msg = 'Usage: `{}remove{} "[{} name]"`'.format(ctx.prefix,l_name.lower(),l_name.lower())
            return await ctx.send(msg)
        safe_name = name.replace("`", "").replace("\\","")
        itemList = self.settings.getServerStat(ctx.guild, l_list)
        if not itemList or itemList == []:
            msg = 'No [[name]]s in list!  You can add some with the `{}add[[name]] "[[[name]] name]" [[[key]]]` command!'.format(ctx.prefix).replace("[[name]]",l_name.lower()).replace("[[key]]",l_key.lower())
            return await ctx.send(msg)
        item = next((x for x in itemList if x["Name"].lower() == name.lower()),None)
        if not item:
            return await ctx.send(Utils.suppressed(ctx,'`{}` not found in {} list!'.format(safe_name,l_name.lower())))
        safe_name = item["Name"].replace("`", "").replace("\\","")
        itemList.remove(item)
        self.settings.setServerStat(ctx.guild, l_list, itemList)
        return await ctx.send(Utils.suppressed(ctx,'`{}` removed from {} list!'.format(safe_name,l_name.lower())))

    async def _item_info(self,ctx,name,l_role="RequiredLinkRole",l_list="Links",l_name="Link",l_key="URL"):
        if name == None:
            msg = 'Usage: `{}info{} "[{} name]"`'.format(ctx.prefix,l_name.lower(),l_name.lower())
            return await ctx.send(msg)
        itemList = self.settings.getServerStat(ctx.guild, l_list)
        if not itemList or itemList == []:
            msg = 'No [[name]]s in list!  You can add some with the `{}add[[name]] "[[[name]] name]" [[[key]]]` command!'.format(ctx.prefix).replace("[[name]]",l_name.lower()).replace("[[key]]",l_key.lower())
            return await ctx.send(msg)
        safe_name = name.replace("`", "").replace("\\","")
        item = next((x for x in itemList if x["Name"].lower() == name.lower()),None)
        if not item:
            return await ctx.send(Utils.suppressed(ctx,'`{}` not found in {} list!'.format(safe_name,l_name.lower())))
        current_time = int(time.time())
        msg = "**{}:**\n".format(item["Name"])
        # Get the info
        created_by = DisplayName.memberForID(item.get("CreatedID",0),ctx.guild)
        created_by = DisplayName.name(created_by) if created_by else item.get("CreatedBy","`UNKNOWN`")
        msg += "Created by: {}\n".format(created_by)
        created    = item.get("Created",None)
        if created:
            msg += "Created: {} ago\n".format(ReadableTime.getReadableTimeBetween(created, current_time, True))
        if item.get("Updated",None):
            updated_by = DisplayName.memberForID(item.get("UpdatedID",0),ctx.guild)
            updated_by = DisplayName.name(updated_by) if updated_by else item.get("UpdatedBy","`UNKNOWN`")
            msg += "Updated by: {}\n".format(updated_by)
            updated    = item.get("Updated",None)
            if created:
                msg += "Updated: {} ago\n".format(ReadableTime.getReadableTimeBetween(updated, current_time, True))
        return await ctx.send(Utils.suppressed(ctx,msg))

    async def _list_items(self,ctx,command,l_role="RequiredLinkRole",l_list="Links",l_name="Link",l_key="URL",raw=False):
        arg_list = ctx.message.content.split()
        if len(arg_list) > 1:
            extra = " ".join(arg_list[1:])
            # We have a random attempt at a passed variable - Thanks Sydney!
            # Invoke this command again with the right name
            return await ctx.invoke(command, name=extra)
        itemList = self.settings.getServerStat(ctx.guild, l_list)
        if not itemList or itemList == []:
            msg = 'No [[name]]s in list!  You can add some with the `{}add[[name]] "[[[name]] name]" [[[key]]]` command!'.format(ctx.prefix).replace("[[name]]",l_name.lower()).replace("[[key]]",l_key.lower())
            return await ctx.send(msg)
        # Sort by link name
        itemList = sorted(itemList, key=lambda x:x['Name'].lower())
        itemText = "**Current {}s:**\n".format(l_name)
        itemText += discord.utils.escape_markdown("\n".join([x["Name"] for x in itemList])) if raw else "\n".join([x["Name"] for x in itemList])
        return await Message.Message(message=Utils.suppressed(ctx,itemText)).send(ctx)

    async def _get_role(self,ctx,l_role="RequiredLinkRole",l_list="Links",l_name="Link",l_key="URL"):
        role = self.settings.getServerStat(ctx.message.guild, l_role)
        if role == None or role == "":
            msg = '**Only Admins** can add and remove {}s.'.format(l_name.lower())
            return await ctx.send(msg)
        # Role is set - let's get its name
        listrole = ctx.guild.get_role(int(role))
        if not listrole:
            return await ctx.send('There is no role that matches id: `{}` - consider updating this setting.'.format(role))
        return await ctx.send(Utils.suppressed(ctx,"You need to be a{} **{}** to add and remove {}s.").format("n" if listrole.name.lower()[0] in "aeiou" else "",Utils.suppressed(ctx,listrole.name),l_name.lower()))
        
    ###                    ###
    ## Link-related Methods ##
    ###                    ###

    # @commands.command(pass_context=True)
    # async def addlink(self, ctx, name : str = None, *, link : str = None):
    #   """Menambahkan link kedalam link list."""
    #   await self._add_item(ctx,name,link,**self.presets["Link"])
        
    # @commands.command(pass_context=True)
    # async def removelink(self, ctx, *, name : str = None):
    #   """Menghapus link dari link list."""
    #   await self._remove_item(ctx,name,**self.presets["Link"])

    # @commands.command(pass_context=True)
    # async def link(self, ctx, *, name : str = None):
    #   """Menampilkan link dari link list."""
    #   await self._get_item(ctx,name,**self.presets["Link"])
        
    # @commands.command(pass_context=True)
    # async def rawlink(self, ctx, *, name : str = None):
    #   """Menampilkan link dari link list dalam bentuk markdown."""
    #   await self._get_item(ctx,name,**self.presets["Link"],raw=True)

    # @commands.command(pass_context=True)
    # async def linkinfo(self, ctx, *, name : str = None):
    #   """Menampilkan informasi mengenai link dari link list."""
    #   await self._item_info(ctx,name,**self.presets["Link"])

    # @commands.command(pass_context=True)
    # async def links(self, ctx):
    #   """Menampilkan semua daftar link dalam link list."""
    #   await self._list_items(ctx,self.link,**self.presets["Link"])
        
    # @commands.command(pass_context=True)
    # async def rawlinks(self, ctx):
    #   """Menampilkan semua daftar link dari link list dalam bentuk markdown."""
    #   await self._list_items(ctx,self.link,**self.presets["Link"],raw=True)

    # @commands.command(pass_context=True)
    # async def linkrole(self, ctx):
    #   """List Lists the required role to add links."""
    #   await self._get_role(ctx,**self.presets["Link"])

    # ###                    ###
    # ## Hack-related Methods ##
    # ###                    ###
    
    # @commands.command(pass_context=True)
    # async def addhack(self, ctx, name : str = None, *, hack : str = None):
    #   """Add a hack to the hack list."""
    #   await self._add_item(ctx,name,hack,**self.presets["Hack"])
        
    # @commands.command(pass_context=True)
    # async def removehack(self, ctx, *, name : str = None):
    #   """Remove a hack from the hack list."""
    #   await self._remove_item(ctx,name,**self.presets["Hack"])

    # @commands.command(pass_context=True)
    # async def hack(self, ctx, *, name : str = None):
    #   """Retrieve a hack from the hack list."""
    #   await self._get_item(ctx,name,**self.presets["Hack"])
        
    # @commands.command(pass_context=True)
    # async def rawhack(self, ctx, *, name : str = None):
    #   """Retrieve a hack's raw markdown from the hack list."""
    #   await self._get_item(ctx,name,**self.presets["Hack"],raw=True)

    # @commands.command(pass_context=True)
    # async def hackinfo(self, ctx, *, name : str = None):
    #   """Displays info about a hack from the hack list."""
    #   await self._item_info(ctx,name,**self.presets["Hack"])

    # @commands.command(pass_context=True)
    # async def hacks(self, ctx):
    #   """List all hack in the hack list."""
    #   await self._list_items(ctx,self.hack,**self.presets["Hack"])
        
    # @commands.command(pass_context=True)
    # async def rawhacks(self, ctx):
    #   """List raw markdown of all hacks in the hack list."""
    #   await self._list_items(ctx,self.hack,**self.presets["Hack"],raw=True)

    # @commands.command(pass_context=True)
    # async def hackrole(self, ctx):
    #   """Lists the required role to add hacks."""
    #   await self._get_role(ctx,**self.presets["Hack"])

    # ###                   ###
    # ## Tag-related Methods ##
    # ###                   ###
    
    # @commands.command(pass_context=True)
    # async def addtag(self, ctx, name : str = None, *, tag : str = None):
    #   """Add a tag to the tag list."""
    #   await self._add_item(ctx,name,tag,**self.presets["Tag"])
        
    # @commands.command(pass_context=True)
    # async def removetag(self, ctx, *, name : str = None):
    #   """Remove a tag from the tag list."""
    #   await self._remove_item(ctx,name,**self.presets["Tag"])

    # @commands.command(pass_context=True)
    # async def tag(self, ctx, *, name : str = None):
    #   """Retrieve a tag from the tag list."""
    #   await self._get_item(ctx,name,**self.presets["Tag"])
        
    # @commands.command(pass_context=True)
    # async def rawtag(self, ctx, *, name : str = None):
    #   """Retrieve a tag's raw markdown from the tag list."""
    #   await self._get_item(ctx,name,**self.presets["Tag"],raw=True)

    # @commands.command(pass_context=True)
    # async def taginfo(self, ctx, *, name : str = None):
    #   """Displays info about a tag from the tag list."""
    #   await self._item_info(ctx,name,**self.presets["Tag"])

    # @commands.command(pass_context=True)
    # async def tags(self, ctx):
    #   """List all tag in the tag list."""
    #   await self._list_items(ctx,self.tag,**self.presets["Tag"])
        
    # @commands.command(pass_context=True)
    # async def rawtags(self, ctx):
    #   """List raw markdown of all tags in the tag list."""
    #   await self._list_items(ctx,self.tag,**self.presets["Tag"],raw=True)

    # @commands.command(pass_context=True)
    # async def tagrole(self, ctx):
    #   """Lists the required role to add tags."""
    #   await self._get_role(ctx,**self.presets["Tag"])
        
    # ###                     ###
    # ## Parts-related Methods ##
    # ###                     ###

    # @commands.command(pass_context=True)
    # async def parts(self, ctx, *, member = None):
    #   """Retrieve a member's parts list. DEPRECATED - Use hw instead."""
    #   if member is None:
    #       member = ctx.message.author
            
    #   if type(member) is str:
    #       memberName = member
    #       member = DisplayName.memberForName(memberName, ctx.guild)
    #       if not member:
    #           msg = 'I couldn\'t find *{}*...'.format(memberName)
    #           return await ctx.send(Utils.suppressed(ctx,msg))
    #   parts = self.settings.getGlobalUserStat(member, "Parts")
    #   if not parts or parts == "":
    #       msg = '*{}* has not added their parts yet!  ~~They can add them with the `{}setparts [parts text]` command!~~ DEPRECATED - Use `{}newhw` instead.'.format(DisplayName.name(member), ctx.prefix, ctx.prefix)
    #       return await ctx.send(msg)
    #   msg = '***{}\'s*** **Parts (DEPRECATED - Use {}hw instead):**\n\n{}'.format(DisplayName.name(member), ctx.prefix, parts)
    #   await ctx.send(Utils.suppressed(ctx,msg))

    # @commands.command(pass_context=True)
    # async def rawparts(self, ctx, *, member = None):
    #   """Retrieve the raw markdown for a member's parts list. DEPRECATED - Use rawhw instead."""
    #   if member is None:
    #       member = ctx.message.author
    #   if type(member) is str:
    #       memberName = member
    #       member = DisplayName.memberForName(memberName, ctx.guild)
    #       if not member:
    #           msg = 'I couldn\'t find *{}*...'.format(memberName)
    #           return await ctx.send(Utils.suppressed(ctx,msg))
    #   parts = self.settings.getGlobalUserStat(member, "Parts")
    #   if not parts or parts == "":
    #       msg = '*{}* has not added their parts yet!  ~~They can add them with the `{}setparts [parts text]` command!~~ DEPRECATED - Use `{}newhw` instead.'.format(DisplayName.name(member), ctx.prefix, ctx.prefix)
    #       return await ctx.send(msg)
    #   parts = discord.utils.escape_markdown(parts)
    #   msg = '***{}\'s*** **Parts (DEPRECATED - Use {}hw instead):**\n\n{}'.format(DisplayName.name(member), ctx.prefix, parts)
    #   await ctx.send(Utils.suppressed(ctx,msg))
        
    # @commands.command(pass_context=True)
    # async def setparts(self, ctx, *, parts : str = None):
    #   """Set your own parts - can be a url, formatted text, or nothing to clear. DEPRECATED - Use newhw instead."""
    #   if not parts:
    #       parts = ""
    #   self.settings.setGlobalUserStat(author, "Parts", parts)
    #   msg = '*{}\'s* parts have been set to (DEPRECATED - Use {}newhw instead):\n{}'.format(DisplayName.name(ctx.author), ctx.prefix, parts)
    #   await ctx.send(Utils.suppressed(ctx,msg))
        
    # @commands.command(pass_context=True)
    # async def partstemp(self, ctx):
    #   """Gives a copy & paste style template for setting a parts list."""
    #   msg = '\{}setparts \`\`\`      CPU : \n   Cooler : \n     MOBO : \n      GPU : \n      RAM : \n      SSD : \n      HDD : \n      PSU : \n     Case : \nWiFi + BT : \n Lighting : \n Keyboard : \n    Mouse : \n  Monitor : \n      DAC : \n Speakers : \`\`\`'.format(ctx.prefix)   
    #   await ctx.send(msg)
        
    @commands.command(pass_context=True)
    async def online(self, ctx):
        """**INDONESIA**
        Menampilkan jumlah member online dalam server.
        
        **ENGLISH**
        Lists the number of users online."""
        cekAuthor = ctx.author
        checkLang = self.settings.getUserStat(cekAuthor, ctx.guild, "Language")
        
        #kalo belum ada language
        if checkLang == None:
            await self.language_not_set(ctx)
        
        members = membersOnline = bots = botsOnline = 0
        for member in ctx.guild.members:
            if member.bot:
                bots += 1
                if not member.status == discord.Status.offline:
                    botsOnline += 1
            else:
                members += 1
                if not member.status == discord.Status.offline:
                    membersOnline += 1
        if checkLang == "ID":
            await Message.Embed(
                title="Member Stats",
                description="Informasi member online server ***{}***".format(ctx.guild.name),
                fields=[
                    { "name" : "Member", "value" : "└─ {:,}/{:,} online ({:,g}%)".format(membersOnline, members, round((membersOnline/members)*100, 2)), "inline" : False},
                    { "name" : "Bot", "value" : "└─ {:,}/{:,} online ({:,g}%)".format(botsOnline, bots, round((botsOnline/bots)*100, 2)), "inline" : False},
                    { "name" : "Total", "value" : "└─ {:,}/{:,} online ({:,g}%)".format(membersOnline + botsOnline, len(ctx.guild.members), round(((membersOnline + botsOnline)/len(ctx.guild.members))*100, 2)), "inline" : False}
                ],
                color=0XFF8C00,
                footer="{}#{}".format(ctx.author.name, ctx.author.discriminator),
                icon_url = "{}".format(ctx.author.avatar_url)).send(ctx)
        if checkLang == "EN":
            await Message.Embed(
                title="Member Stats",
                description="Current member information for ***{}***".format(ctx.guild.name),
                fields=[
                    { "name" : "Member", "value" : "└─ {:,}/{:,} online ({:,g}%)".format(membersOnline, members, round((membersOnline/members)*100, 2)), "inline" : False},
                    { "name" : "Bot", "value" : "└─ {:,}/{:,} online ({:,g}%)".format(botsOnline, bots, round((botsOnline/bots)*100, 2)), "inline" : False},
                    { "name" : "Total", "value" : "└─ {:,}/{:,} online ({:,g}%)".format(membersOnline + botsOnline, len(ctx.guild.members), round(((membersOnline + botsOnline)/len(ctx.guild.members))*100, 2)), "inline" : False}
                ],
                color=0XFF8C00,
                footer="{}#{}".format(ctx.author.name, ctx.author.discriminator),
                icon_url = "{}".format(ctx.author.avatar_url)).send(ctx)


    @commands.command(pass_context=True)
    async def lastonline(self, ctx, *, member = None):
        """**INDONESIA**
        Melihat member terakhir online.
        
        **ENGLISH**
        Lists the last time a user was online.

        Contoh \ Example:
        acx lastonline @ACX•NvStar
        acx lastonline ACX•NvStar#9110
        acx lastonline ACX•NvStar
        """
        cekAuthor = ctx.author
        checkLang = self.settings.getUserStat(cekAuthor, ctx.guild, "Language")
        
        #kalo belum ada language
        if checkLang == None:
            await self.language_not_set(ctx)
        
        if not member:
            if checkLang == "ID":
                em = discord.Embed(color = 0XFF8C00, description =  "Melihat informasi member terakhir online\n\n"
                                                                    "**Panduan**\n"
                                                                    "*`{}lastonline [member]`*\n\n"
                                                                    "*Catatan:*"
                                                                    "*`member` dapat berupa mention, nama, atau nickname.*\n"
                                                                    "*ketik `{}help lastonline` untuk informasi lebih lanjut.*"
                                                                    .format(ctx.prefix,
                                                                            ctx.prefix))
                em.set_footer(text = "Saat mengetik command, tanda [] tidak usah digunakan\n{}#{}".format(ctx.author.name, ctx.author.discriminator),
                              icon_url = "{}".format(ctx.author.avatar_url))
                return await ctx.send(embed = em)

            if checkLang == "EN":
                msg  = "Lists the last time a user was online.\n\n"
                msg += "**Usage**\n"
                msg += "*`{}lastonline [member]`*\n\n".format(ctx.prefix)
                msg += "*Note : you can type `member` as mention someone, nickname, or username.*"
                em = discord.Embed(color = 0XFF8C00, description = msg)
                em.set_footer(text = "When typing commands, you don't need to use the [] sign\n{}#{}".format(ctx.author.name, ctx.author.discriminator),
                              icon_url = "{}".format(ctx.author.avatar_url))
                return await ctx.send(embed = em)

        if type(member) is str:
            memberName = member
            member = DisplayName.memberForName(memberName, ctx.guild)
            if not member:
                if checkLang == "ID":
                    msg = '┐(￣ヘ￣;)┌\nAku tidak dapat menemukan *{}*...'.format(memberName)
                    em = discord.Embed(color = 0XFF8C00, description = msg)
                    em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                                  icon_url = "{}".format(ctx.author.avatar_url))
                    return await ctx.send(embed = em)
                    #return await ctx.send(Utils.suppressed(ctx,msg))
                
                if checkLang == "EN":
                    msg = '┐(￣ヘ￣;)┌\nI can\'t find *{}*...'.format(memberName)
                    em = discord.Embed(color = 0XFF8C00, description = msg)
                    em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                                  icon_url = "{}".format(ctx.author.avatar_url))
                    return await ctx.send(embed = em)
        
        name = DisplayName.name(member)

        # lanjut kebawah ini kalo sudah pilih bahasa
        if not member.status == discord.Status.offline:
            if checkLang == "ID":
                msg = '*{}* sedang online.'.format(member.mention)
            if checkLang == "EN":
                msg = '*{}* is online.'.format(member.mention)
        else:
            lastOnline = self.settings.getUserStat(member, ctx.guild, "LastOnline")
            if lastOnline == "Unknown":
                self.settings.setUserStat(member, ctx.guild, "LastOnline", None)
                lastOnline = None
            if lastOnline:
                if checkLang == "ID":
                    currentTime = int(time.time())
                    timeString  = ReadableTime.getReadableTimeBetween(int(lastOnline), currentTime, True)
                    msg = 'Terakhir aku lihat {} online\n*{} yang lalu*.'.format(member.mention, timeString)
                if checkLang == "EN":
                    currentTime = int(time.time())
                    timeString  = ReadableTime.getReadableTimeBetweenEng(int(lastOnline), currentTime, True)
                    msg = 'The last time I saw *{}* was\n*{} ago*'.format(member.mention, timeString)
            else:
                if checkLang == "ID":
                    msg = '┐(￣ヘ￣;)┌\nAku tidak tau kapan *{}* terakhir online.'.format(member.mention)
                if checkLang == "EN":
                    msg = '┐(￣ヘ￣;)┌\nI don\'t know when *{}* was last online.'.format(member.mention)
        em = discord.Embed(color = 0XFF8C00, description = msg)
        em.set_footer(text = "{}#{}".format(ctx.author.name, ctx.author.discriminator),
                      icon_url = "{}".format(ctx.author.avatar_url))
        await ctx.send(embed = em)

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