import discord
from discord.ext import commands
import random


def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if minutes == 0:
        return f'{seconds} seconds'
    return f'{minutes} minutes {seconds} seconds'


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="vote",
                            description="Vote the one who is sus",
                            guild_ids=[720657696407420950])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def vote(self,
                   ctx,
                   member: discord.Member = commands.Param(
                       description="This person is sus", default=False)):
        if not member:
            member = ctx.author
        if ctx.channel.id != 759526501598101506:
            self.vote.reset_cooldown(ctx)
            return await ctx.response.send_message(
                "You can't use this here try it in <#759526501598101506>",
                ephemeral=True)
        bools = ["was%20The%20Imposter.", "was%20Not%20The%20Imposter."]
        colors = [
            "blue", "brown", "yellow", "green", "red", "orange", "lime",
            "pink", "blue", "darkblue"
        ]
        name = member.name.replace(" ", "%20")
        await ctx.response.send_message(
            f"https://engineer15.sirv.com/Images/Among%20Us/{random.choice(colors)}.png?text={name}%20"
            f"{random.choice(bools)}&text.size=40&text.color=0D0D0D&text."
            f"position.gravity=center&text.position.x=0%&text.position.y=15%")

    @vote.error
    async def vote_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            try:
                return await ctx.response.send_message(
                f":warning: You Cannot Vote for another: {convert(int(error.retry_after))}.",
                ephemeral=True)
            except discord.InteractionResponded:
                pass
        if isinstance(error , commands.MemberNotFound):
            try:
                return await ctx.response.send_message("That member isnt in the server",ephemeral=True)
            except discord.InteractionResponded:
                pass

def setup(bot):
    print("Loaded Fun")
    bot.add_cog(fun(bot))
