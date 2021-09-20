import discord
from discord.ext import commands
import random
from discord_slash import SlashCommand
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

client = commands.Bot(command_prefix='.', case_insensitive=True)
slash = SlashCommand(client, sync_commands=True, override_type=True, sync_on_cog_reload=True,
                     delete_from_unused_guilds=True)
def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if minutes == 0:
        return f'{seconds} seconds'
    return f'{minutes} minutes {seconds} seconds'



class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="vote",
        description="Vote the one who is sus",
        guild_ids=[720657696407420950],
        options=[
            create_option(
                name="member",
                description="This person is sus",
                option_type=6,
                required=False
            )
        ]
    )
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def vote(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        if ctx.channel.id != 759526501598101506:
            self.vote.reset_cooldown(ctx)
            return await ctx.send("You can't use this here try it in <#759526501598101506>", hidden=True)
        bools = ["was%20The%20Imposter.", "was%20Not%20The%20Imposter."]
        colors = ["blue", "brown", "yellow", "green", "red", "orange", "lime", "pink", "blue", "darkblue"]
        name = member.name.replace(" ", "%20")
        await ctx.send(
            f"https://engineer15.sirv.com/Images/Among%20Us/{random.choice(colors)}.png?text={name}%20"
            f"{random.choice(bools)}&text.size=40&text.color=0D0D0D&text."
            f"position.gravity=center&text.position.x=0%&text.position.y=15%")

    @vote.error
    async def vote_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":warning: You Cannot Vote for another: {convert(int(error.retry_after))}.", hidden=True)


def setup(client):
    print("Loaded Fun")
    client.add_cog(fun(client))