import discord
from discord.ext import commands
import os
import keep_alive


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=".",
    case_insensitive=True,
    intents=intents,
    strip_after_prefix=False,
    self_bot=False,
    sync_permissions=True,
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

for filename in os.listdir('./slash'):
    if filename.endswith('.py'):
        bot.load_extension(f'slash.{filename[:-3]}')

keep_alive.keep_alive()
token = os.getenv("TOKEN")

print(f"DPG Bot Py is Live!\ndiscord.py version {discord.__version__}\n")

bot.run(token)
