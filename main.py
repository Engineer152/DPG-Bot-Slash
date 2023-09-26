import os
#import keep_alive
from os import kill
from dotenv import load_dotenv

try:
    import discord
except Exception:
    kill(1,15)
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix="-",
    case_insensitive=True,
    intents=intents,
    strip_after_prefix=False,
    owner_ids={709424341913174077,548530397034577930,750488246542139433},
    command_sync_flags = commands.CommandSyncFlags.all(),
    activity=discord.Activity(type=discord.ActivityType.listening, name='-help'),
)

bot.remove_command("help")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
#bot.unload_extension('cogs.leveling')

#bot.load_extension("cogs.admin")

for filename in os.listdir('./slash'):
    if filename.endswith('.py'):
        bot.load_extension(f'slash.{filename[:-3]}')
        
#bot.load_extension('jishaku')
#os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

@bot.command()
@commands.has_any_role(756176148001456168,756183369406087208,756176241467326628)
async def load(ctx, cog):
    try:
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog.title()} was reloaded")
    except commands.ExtensionNotLoaded:
        await ctx.send('That extention is already loaded')




@bot.command()
@commands.has_any_role(756176148001456168,756183369406087208,756176241467326628)
async def unload(ctx, cog):
    try:
        bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"{cog.title()} was Unloaded")
    except commands.ExtensionNotLoaded:
        await ctx.send('That extention is already unloaded')





@bot.command()
@commands.has_any_role(756176148001456168,756183369406087208,756176241467326628)
async def reload(ctx, cog):
    bot.reload_extension(f"cogs.{cog}")
    await ctx.send(f"{cog.title()} was reloaded")

@load.error
@unload.error
@reload.error
async def loader_error(ctx, error):
    if isinstance(error,commands.CheckFailure):
        return
    if isinstance(error,commands.MissingAnyRole):
        return
    print(error)

#keep_alive.keep_alive()
token = os.getenv("TOKEN")
@bot.event
async def on_slash_command_error(ctx,error):
    print(error)

#@bot.slash_command_check_once
#async def blacklist(ctx):
#    roles = []
#    for i in ctx.author.roles:
#        roles.append(i.id)
#    if 788494319459500042 in roles:
#        return True


print(f"DPG Bot Py is Live!\ndiscord.py version {discord.__version__}\n")

try:
    bot.run(token)
    #bot.run(token) # Replace this with your usual `bot.run` line
except discord.HTTPException as err:
    if err.status == 429:
         #  Check if the status code is 429, only then will the repl will be killed.
        print("Rate-limit detected. Restarting the repl.")
        kill(1, 15)  # send the signal
    print(err[37])
