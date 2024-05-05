import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(723187777465876543)
    async def chstatus(self, ctx: commands.Context, act, *, nm):
        if act == "watch":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=nm))
            nm = "Watching"
        if act == "listen":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=nm))
            act = "Listening to"

        if act == "stream":
            await self.bot.change_presence(
                activity=discord.Streaming(name=nm, url="http://twitch.tv/dudeperfectgaming"))
            act = "Streaming"

        print("Status Changed")
        await ctx.send(f'Status changed to: {act} {nm}')

    @chstatus.error
    async def chstatus_error(self, ctx: commands.Context, error):
        await ctx.send(error)
        # await ctx.send('You are not the developer')


###########################################################    
###########################################################
########FOR IRONMAN TO USE ONLY JUST A FEW CHECKS##########
########AND FOR DELETING BOTS DM MESSAGES #################
###########################################################
###########################################################
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.channel_id == 801469012528594944:
            if "https://" not in payload.cached_message.content:
                user = await self.bot.fetch_user(548530397034577930)
                await user.send(f"⚠ Deletion detected ⚠\nDeletion by: {payload.cached_message.author },{payload.cached_message.author.id }\nMessage Content:{payload.cached_message.content }")

    @commands.command()
    @commands.is_owner()
    @commands.dm_only()
    async def msgdel(self,ctx:commands.Context,amount:int=10):
        def is_me(m):
            return m.author == self.bot.user
        deleted = await channel.purge(limit=amount, check=is_me)
        await channel.send(f'Deleted {len(deleted)} message(s)',delete_after=5)


    @msgdel.error
    async def msgdel_error(self, ctx: commands.Context, error):
        await ctx.send(error)

def setup(bot):
    print("Loaded Admin")
    bot.add_cog(Admin(bot))
