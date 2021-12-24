import discord
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="rules",
        description="The list of all server rules you must abide by.",
        guild_ids=[720657696407420950]
    )
    async def rules(self, ctx):
        embed = discord.Embed(
            title="DPGN SERVER RULES",
            description="By entering this server and verifying, "
                        "you have agreed to all rules laid out within the rules channel. "
                        "If you cannot follow these <#723279473960681473> you will be warned. "
                        "Multiple warnings may result in a permanent ban."
        )
        embed.set_thumbnail(url="https://i.ibb.co/bLJR1Zz/Know-the-Rules-320x242.png")
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        name="youtube",
        description="Do you follow the Dude Perfect YouTube Channel yet?!",
        guild_ids=[720657696407420950]
    )
    async def youtube(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(title="Dude Perfect YouTube Channels", color=0x46e2ec,
                              description='Make sure to Subscribe to all three channels!\n\n'
                                          '[Dude Perfect](https://www.youtube.com/dudeperfect)\n'
                                          '[Dude Perfect Plus](https://www.youtube.com/dudeperfectplus)\n'
                                          '[Dude Perfect Gaming](https://www.youtube.com/dudeperfectgaming)')

        embed.set_thumbnail(url="https://i.imgur.com/nJXVOIq.png")
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        name="social",
        description="Check out the Dudes on their Socials!",
        guild_ids=[720657696407420950]
    )
    async def social(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.send("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(title='Socials', description="Check out the Dude's socials", color=0x46e2ec)
        embed.add_field(name='INSTAGRAM',
                        value='Check out them on Instagram\n[Dude Perfect](https://www.instagram.com/dudeperfect)\n[Dude Perfect Gaming](https://www.instagram.com/dudeperfectgaming)\n[Dude Perfect Editors](https://www.instagram.com/dpeditors/)\n[Coby](https://www.instagram.com/cobycotton)\n[Cody](https://www.instagram.com/cody_jones_)\n[Cory](https://www.instagram.com/corycotton)\n[Garrett](https://www.instagram.com/garretthilbert)\n[Tyler](https://www.instagram.com/tylerntoney)\n[Sparky](https://www.instagram.com/sparky_man4)')
        embed.add_field(name='TIKTOK',
                        value='Check out them on TikTok\n[Dude Perfect](https://www.tiktok.com/@dudeperfect)')
        embed.add_field(name='TWITTER',
                        value='Check out them on Twitter\n[Dude Perfect](https://www.twitter.com/dudeperfect)\n[Cory](https://twitter.com/CoryCotton)\n[Coby](https://twitter.com/CobyCotton)\n[Cody](https://twitter.com/Codes87)\n[Garrett](https://twitter.com/GarrettHilbert)\n[Tyler](https://twitter.com/TylerNToney)')
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        name="tiethepie",
        description="One day we will know the true Panda identity!",
        guild_ids=[720657696407420950]
    )
    async def tiethepie(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(title="**Tie The Pie**", color=0x46e2ec,
                              description='Subscribe to Dude Perfect to see the reveal of Panda\n**[Details](https://youtu.be/bFUZ5gruc0E)**ㅤㅤㅤㅤ**[Subscribe](http://bit.ly/SubDudePerfect)**')
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(description="Information about the DP Beans", guild_ids=[720657696407420950])
    async def dpbeans(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(title="<:DPBeans:816310052595433512:DUDE PERFECT BEANS!!<:DPBeans:816310052595433512:",
                              description="Practice makes perfect. We lost track of how many different versions we "
                                          "made, but we call it Batch 5 as a nod to our 5 friends at DudePerfect. "
                                          "They helped us create the perfect bean…made with applewood smoked bacon, "
                                          "authentic Southwestern spice and real jalapeños for a robust not-too-hot "
                                          "flavor. Pound It Noggin!\n\n[DUDE PERFECT JALAPEÑO & BACON BEANS 12 PACK]("
                                          "https://seriousbeanco.com/products/dude-perfect-jalapeno-bacon-beans-12"
                                          "-pack) ",
                              color=0x46e2ec)
        embed.set_thumbnail(url="https://i.ibb.co/JzRdVkr/Serious-Bean-Co-Jalapeno-Bacon-Article.png")
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(description="The Overtime intro", guild_ids=[720657696407420950])
    async def intro(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(
            description=":musical_note:\nTall Guy, Beard, Twins, Purple Hoser\n\nDude Perfect's in Overtime\n\nTall "
                        "Guy, Beard, Twins, Purple Hoser\n\nNow we're heading onto Overtime\n:musical_note:",
            color=0x5fb71b, title="OVERTIME")
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(description="Wanna watch all vids? You should check this out",guild_ids=[720657696407420950])
    async def playlist(self, ctx):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        embed = discord.Embed(title="YOUTUBE PLAYLIST",
                              description="[Here is a playlist of all of Dude Perfects Vids!]("
                                          "https://www.youtube.com/watch?v=OFBsuEGhQkI&list=PLCsuqbR8ZoiDF6iBf3Zw6v1jYBNRfCuWC)",
                              color=0x46e2ec)
        await ctx.response.send_message(embed=embed)

def setup(bot):
    print("Loaded Info")
    bot.add_cog(info(bot))
