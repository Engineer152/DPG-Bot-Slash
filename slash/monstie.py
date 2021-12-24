import discord
from discord.ext import commands
import random


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return f'{hour} hours {minutes} minutes {seconds} seconds'


def is_certified(message):
    roles = message.author.roles
    role_ids = []
    for i in roles:
        role_ids.append(i.id)
    nocd = [723187777465876543, 763044012755779664, 768509120525107230, 757760951620468817]
    for i in nocd:
        if i in role_ids:
            return
    return commands.cooldown(1, 3600, commands.BucketType.guild)


class monsties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="chatmonstie",
        description="To wake the chat up when its sleepy",
        guild_ids=[720657696407420950])
    @commands.dynamic_cooldown(is_certified)
    async def chatmonstie(self, ctx):
        with open("questions.txt") as questions:
            lines = []
            for line in questions:
                lines.append(line)

        embed = discord.Embed(title=f'{random.choice(lines)}', color=0x46e2ec)
        embed.add_field(name='This chat is a little sleepy.',
                        value='Answer the question to give the chat a little pep. How energizing...just'
                              ' like Sparky drinking a monstie.')
        embed.set_image(url='https://c.tenor.com/QnuCAgTY6dUAAAAi/amongus-amandarling.gif')
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        name="monstie",
        description="Check your monstie crack with the official 'Monstie-Meter'",
        guild_ids=[720657696407420950]
    )
    @commands.cooldown(1, 28800, commands.BucketType.user)
    async def monstie(self, ctx):
        if ctx.channel.id != 758297067155488799 or ctx.channel.id != 757761322862510122:
            if self.monstie.get_cooldown_retry_after == 0.0:
                self.monstie.reset_cooldown(ctx)
            return await ctx.reponse.send_message("Please use it in the correct channel", ephemeral=True)
        embed = discord.Embed(title="**MONSTIE METER**",
                              description=f"{ctx.author.mention}'s Monstie crack scored a {random.randint(0, 6)} on the Monstie Meter!",
                              color=0xf0f0f0)
        embed.set_thumbnail(url='https://i.ibb.co/rsbPWmk/whitemonstie.png?width=283&height=701')
        await ctx.response.send_message(embed=embed)

    @cog_ext.cog_slash(name="mvpmonstie", description="Check your monstie crack with the official 'MVP Monstie-Meter'"
        , guild_ids=[720657696407420950])
    @commands.cooldown(1, 28800, commands.BucketType.user)
    async def mvpmonstie(self, ctx):
        if ctx.channel.id != 758297067155488799 or ctx.channel.id != 757761322862510122:
            if self.monstie.get_cooldown_retry_after == 0.0:
                self.monstie.reset_cooldown(ctx)
            return await ctx.response.send_message("Please use it in the correct channel", ephemeral=True)
        embed = discord.Embed(title="**MVP MONSTIE METER**",
                              description=f"{ctx.author.mention}'s Monstie crack scored a {random.randint(9, 13)} on the Monstie Meter!",
                              color=0xe4d00a)
        embed.set_thumbnail(url='https://i.ibb.co/McRhw2y/Monstie-Gold.png')
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(name="adminmonstie",
                            description="Check your monstie crack with the official 'Admin Monstie-Meter'"
        , guild_ids=[720657696407420950], default_permission=False)
    @commands.guild_permissions(720657696407420950,
                                roles={723187777465876543: True, 763044012755779664: True, 768509120525107230: True})
    async def adminmonstie(self, ctx):
        embed = discord.Embed(title="**ADMIN MONSTIE METER**",
                              description=f"{ctx.author.mention}'s Monstie crack scored a {random.randint(15, 30)} on the Monstie Meter!",
                              color=0x6699cc)
        embed.set_thumbnail(
            url='https://www.monsterenergy.com/media/uploads_image/2020/01/22/auto/800/2811c4db068e6afbeaf6f0fcf36769b1.png?mod=v1_90fd6dec396a042bd0cdd25ddbce6f14')
        await ctx.response.send_message(embed=embed)

    @monstie.error
    @mvpmonstie.error
    @chatmonstie.error
    @adminmonstie.error
    async def monstie_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.response.send_message(
                f"You can crack your next Monstie in {convert(int(error.retry_after))}.\nToo many Monsties isn't good for your health...",
                ephemeral=True)


def setup(bot):
    print("Loaded Monsties")
    bot.add_cog(monsties(bot))
