import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.',case_insensitive=True)

class Admin(commands.Cog):
  def __init__(self,client):
    self.client=client

  @commands.command()
  #@commands.is_owner()
  @commands.has_any_role(723187777465876543)
  async def chstatus(self,ctx,act,*,nm):
    if act == "watch":
      await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=nm))
      nm="Watching"
    if act == "listen":
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=nm))
        act="Listening to"
                
    if act == "stream":
        await self.client.change_presence(activity=discord.Streaming(name=nm, url="http://twitch.tv/dudeperfectgaming"))
        act="Streaming"
        #await self.client.change_presence(activity=discord.Game(name=nm))
        
    print("Status Changed")
    await ctx.send(f'Status changed to: {act} {nm}')

  @chstatus.error
  async def chstatus_error(self,ctx, error): 
    await ctx.send(error)
    #await ctx.send('You are not the developer')

def setup(client):
    print("Loaded Admin")
    client.add_cog(Admin(client))