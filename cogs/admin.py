import discord
from discord.ext import commands




class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(723187777465876543)
    async def chstatus(self, ctx, act, *, nm):
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
    async def chstatus_error(self, ctx, error):
        await ctx.send(error)
        # await ctx.send('You are not the developer')


def setup(bot):
    print("Loaded Admin")
    bot.add_cog(Admin(bot))
