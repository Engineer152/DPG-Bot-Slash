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

    @commands.slash_command(description="Call an emergency meeting",
                            guild_ids=[720657696407420950])
    async def button(self, ctx, *, txt=None):
        if ctx.channel.id != 759526501598101506:
            self.vote.reset_cooldown(ctx)
            return await ctx.response.send_message(
                "You can't use this here try it in <#759526501598101506>",
                ephemeral=True)

        if txt is None:
            txt = "%20"
        name = txt.replace(" ", "%20")
        await ctx.send(f"https://vacefron.nl/api/emergencymeeting?text={name}")

    @vote.error
    async def vote_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            try:
                return await ctx.response.send_message(
                    f":warning: You Cannot Vote for another: {convert(int(error.retry_after))}.",
                    ephemeral=True)
            except discord.InteractionResponded:
                pass
        if isinstance(error, commands.MemberNotFound):
            try:
                return await ctx.response.send_message("That member isnt in the server", ephemeral=True)
            except discord.InteractionResponded:
                pass

    @commands.slash_command(
        name="bottlebust",
        description="Bottle Bust an un-expecting friend!",
        guild_ids=[720657696407420950])
    async def _bottlebust(self, ctx, frenemy: discord.Member = commands.Param(description="Who will you bottle bust?",
                                                                              default=False)):
        if ctx.channel.id != 758297067155488799:
            return await ctx.respose.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        if not frenemy:
            frenemy = ctx.author
        embed = discord.Embed(title=":rotating_light:             BOTTLE BUSTER ALERT            :rotating_light:",
                              description=f"{ctx.author.mention} **BOTTLE BUSTED** {frenemy.mention}")
        embed.set_image(url='https://i.ibb.co/x3899w9/Ty-BB.gif')
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(description="It's time for a dance party!", guild_ids=[720657696407420950], name="dance")
    async def _dance(self, ctx):
        embed = discord.Embed(title='PANDA DANCE PARTY!')
        embed.set_image(url='https://media.tenor.com/images/b0dcde6ad525effd15648871cf6810f6/tenor.gif')
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(name="cf", description=" Heads or tails, let the DPG BOT decide!",
                            guild_ids=[720657696407420950])
    async def _cf(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        x = random.randint(1, 2)
        if x == 1:
            embed = discord.Embed(title="You flipped a...", color=0x46e2ec)
            embed.set_image(url='https://i.ibb.co/Y3zVhL3/CFHeads.gif')
            await ctx.response.send_message(embed=embed)
            await asyncio.sleep(5)
            embed.set_image(url='https://i.ibb.co/Y3zVhL3/CFHeads.gif')
            embed.set_footer(text="HEADS")
            await ctx.edit_original_message(embed=embed)
        elif x == 2:
            embed = discord.Embed(title="You flipped a...", color=0x46e2ec)
            embed.set_image(url='https://i.ibb.co/bRpbPcd/CFTails.gif')
            await ctx.response.send_message(content=None, embeds=[embed])
            await asyncio.sleep(5)
            embed.set_footer(text="TAILS")
            embed.set_image(url='https://i.ibb.co/bRpbPcd/CFTails.gif')
            await ctx.edit_original_message(embed=embed)

    @commands.slash_command(description="Take your chance at an awesome DP trickshot. Can you do it?!",
                            guild_ids=[720657696407420950])
    async def trickshot(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        rng = random.randint(0, 5)
        if rng == 5:
            with open("gtrickshot.txt") as questions:
                lines = []
                for line in questions:
                    lines.append(line)
            embed = discord.Embed(title=f'{lines[random.randint(0, len(lines) - 1)]}', color=0x5fb71b)
            await ctx.reponse.send_message(embed=embed)
        else:
            with open("btrickshot.txt") as questions:
                lines = []
                for line in questions:
                    lines.append(line)
            embed = discord.Embed(title=f'{lines[random.randint(0, len(lines) - 1)]}', color=0xe74c3c)
            await ctx.response.send_message(embed=embed)

    @commands.slash_command(name="signoff", description="Heading out? Hit us with the DP Sign-off!",
                            guild_ids=[720657696407420950])
    async def _signoff(self, ctx):
        embed = discord.Embed(description=f'**{ctx.author.mention} is signing off for now...**', color=0x46e2ec)
        embed.add_field(name='POUND IT! :punch:', value='\u200b', inline=False)
        embed.add_field(name='NOGGIN! :busts_in_silhouette:', value='\u200b', inline=False)
        embed.add_field(name='SEE YA!! :v:', value='\u200b', inline=False)
        embed.add_field(name=':billed_cap:     :arrow_right:     :movie_camera:', value='\u200b', inline=False)
        embed.set_image(
            url="http://media.discordapp.net/attachments/821907733434597386/824039035424866344/giphy-downsized-medium.gif")
        await ctx.response.send_message(embed=embed)
        message = await ctx.original_message()
        await message.add_reaction('\U0001f44b')

    @commands.slash_command(description="Learn all there is to know about the dudes!", guild_ids=[720657696407420950])
    async def dpwiki(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(title='DP WIKI',
                              description='[This](https://dudeperfect.fandom.com/wiki/Dude_Perfect_Wiki) is an '
                                          'awesome resource for all of the Dude Perfect stats and info!',
                              color=0x46e2ec)
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(description="Come join the DPG Minecraft Community Server!", name="minecraftserver",
                            guild_ids=[720657696407420950])
    async def _minecraftserver(self, ctx):
        embed = discord.Embed(title="DPG MINECRAFT SERVER",
                              description="Below you can find information on how to connect to the official: **DPG "
                                          "Minecraft Server**",
                              color=0x46e2ec)
        embed.add_field(name="__Supported Consoles:__",
                        value="- Java Version\n- Windows 10 Bedrock\n- Xbox\n- Nintendo Switch\n- Android or Iphone",
                        inline=False)
        embed.add_field(name="__IP Address:__",
                        value="IP Address: dpgaming.serveminecraft.net\n**NOTE: the address is 'serve' NOT "
                              "'server'**\nPort: 25565\n\nPlease watch the following instructional video for "
                              "connecting to the DPG Minecraft Server: [HOW TO]("
                              "https://www.youtube.com/watch?v=hnO1PFVvbmI)\nIf you ever need any help at all please "
                              "go to the #minecraft channel in [DPG Nation server](https://discord.gg/A68YFtC). You "
                              "may ping @Minecraft Mod at any time. This is a cross platform server between all "
                              "devices that are currently available above. If you are on Bedrock Edition you will be "
                              "marked with 'BR_' to indicate your a bedrock player playing on our Java "
                              "Server.\n\nUnfortunately you will not be able to use custom skins if you are on "
                              "Bedrock. We will keep you updated on any changes in the future.")
        await ctx.response.send_message(":mailbox: You've Got Mail!", ephemeral=True)
        try:
            message = await ctx.author.send(embed=embed)
        except discord.Forbidden:
            return await ctx.edit_original_message(
                content="Error! Your DM's (Direct Message's) are closed so I couldn't send you the message ")
        await ctx.edit_original_message(
            content=f"[Click here to view your mail :mailbox:]({message.jump_url})")

def setup(bot):
    print("Loaded Fun")
    bot.add_cog(fun(bot))
