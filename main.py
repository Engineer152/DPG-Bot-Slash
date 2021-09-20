import discord
from discord.ext import commands
import os, asyncio
import keep_alive
from discord_slash import SlashCommand

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix=".",
    case_insensitive=True,
    intents=intents,
    strip_after_prefix=False,
    self_bot=False,
    activity=discord.Activity(type=discord.ActivityType.listening, name='-help'),
)
slash = SlashCommand(client, sync_commands=True, override_type=True, sync_on_cog_reload=True,
                     delete_from_unused_guilds=True)
client.remove_command("help")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./slash'):
    if filename.endswith('.py'):
        client.load_extension(f'slash.{filename[:-3]}')

keep_alive.keep_alive()
token = os.getenv("TOKEN")

print(f"DPG Bot Py is Live!\ndiscord.py verion {discord.__version__}")

client.run(token)
