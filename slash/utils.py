import discord
import datetime
from discord.ext import commands

import pickle


def badwords():
    with open("./swear_words.dat", "rb") as file:
        bad = pickle.load(file)
    verybad = []
    for i in bad:
        verybad.append(i.strip())
    return verybad


def checkforbad(message):
    bad = badwords()
    for i in range(len(bad)):
        if bad[i] in message.split():
            return False
    return True


class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="welcome",
                            description="Welcome someone to the server",
                            guild_ids=[720657696407420950])
    async def _welcome(self,
                       ctx,
                       member: discord.Member = commands.Param(
                           description="Who is new here", default=False)):
        if not member:
            embed = discord.Embed(
                description=
                f"**WELCOME TO {ctx.guild.name}\nCheck <#723279473960681473> "
                f"and <#732263314461032529> to get started**\n\nWelcome **New Member**!",
                color=discord.Color.random())
            try:
                embed.set_image(url=ctx.guild.icon)
            except Exception:
                pass
            await ctx.response.send_message(embed=embed)
        if member:
            embed = discord.Embed(
                description=
                f"**WELCOME TO {ctx.guild.name}\nCheck <#723279473960681473> "
                f"and <#732263314461032529> to get started**\n\nWelcome **{member.name}**!",
                color=discord.Color.random())
            try:
                embed.set_image(url=ctx.guild.icon)
            except Exception:
                pass
            await ctx.response.send_message(content=f"{member.mention}",
                                            embed=embed)

    @commands.slash_command(name="poll",
                            description="Ask a question to your friends",
                            guild_ids=[720657696407420950])
    @commands.cooldown(1, 1800, commands.BucketType.member)
    async def _poll(
        self,
        ctx,
        question: str = commands.Param(description="This is the question."),
        first: str = commands.Param(description="This is the 1st option."),
        second: str = commands.Param(description="This is the 2nd option.",
                                     default=False),
        third: str = commands.Param(description="This is the 3rd option.",
                                    default=False),
        fourth: str = commands.Param(description="This is the 4th option.",
                                     default=False),
        fifth: str = commands.Param(description="This is the 5th option.",
                                    default=False),
        sixth: str = commands.Param(description="This is the 6th option.",
                                    default=False),
        seventh: str = commands.Param(description="This is the 7th option.",
                                      default=False),
        eighth: str = commands.Param(description="This is the 8th option.",
                                     default=False),
        ninth: str = commands.Param(description="This is the 9th option.",
                                    default=False),
        tenth: str = commands.Param(description="This is the 10th option.",
                                    default=False)):
        if not checkforbad(question):
            return await ctx.response.send_message(
                f"{ctx.author.mention}  **That word is not allowed in this server.**",
                ephemeral=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,users=False))
        options = [
            first, second, third, fourth, fifth, sixth, seventh, eighth, ninth,
            tenth
        ]
        final_options = ""
        for i in options:
            if i :
                if not checkforbad(i):
                    return await ctx.response.send_message(
                        f"{ctx.author.mention}  **That word is not allowed in this server.**",
                        ephemeral=True)
            if not i :
                continue

        for i in range(len(options)):
            if not options[i]:
                continue
            final_options += f"{i + 1}. {options[i]}\n"

        embed = discord.Embed(title=question,
                              description=final_options,
                              color=0x46e2ec)
        if ctx.author.guild_avatar:
            embed.set_author(name=ctx.author, icon_url=ctx.author.guild_avatar)
        else:
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

        await ctx.response.send_message(
            content=f"{ctx.author.mention} **Your poll has been put up.**",
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,users=False))

        reactions = [
            "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"
        ]
        poll_channel = self.bot.get_channel(730882815381733459)

        msg = await poll_channel.send(embed=embed)
        a = 0
        for v in range(len(options)):
            if not options[v]:
                a += 1
                continue
            await msg.add_reaction(reactions[a])
            a += 1

    @commands.slash_command(
        name="suggest",
        description="Suggest something to be added in the server",
        guild_ids=[720657696407420950])
    @commands.cooldown(1, 1800, commands.BucketType.member)
    async def _suggest(self,
                       ctx,
                       suggestion: str = commands.Param(
                           description="This is the suggestion.")):
        if not checkforbad(suggestion):
            return await ctx.response.send_message(
                f"{ctx.author.mention}  **That word is not allowed in this server.**",
                ephemeral=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,users=False))
        suggest_channel = self.bot.get_channel(725000413358587984)
        embed = discord.Embed(description=suggestion,
                              color=0x89aa00,
                              timestamp=datetime.datetime.utcnow())
        if ctx.author.guild_avatar:
            embed.set_author(name=ctx.author, icon_url=ctx.author.guild_avatar)
        else:
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.response.send_message(
            content=
            f"{ctx.author.mention} **Your suggestion has been submitted.**",
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,users=False))
        suggest = await suggest_channel.send(embed=embed)
        await suggest.add_reaction("👍")
        await suggest.add_reaction("👎")

    @commands.slash_command(
        name="suggestsong",
        description="Suggest some song to be added in the bot of this server",
        guild_ids=[720657696407420950])
    async def _suggestsong(
        self,
        ctx,
        name: str = commands.Param(description="Name of the song"),
        artist: str = commands.Param(description="Artist's name"),
        where: str = commands.Param(
            description="Name of the DP video that has the song in it"),
        recording: str = commands.Param(
            description="Link to a Video/Recording of just the song")):
        stuff = ["Name", "Artist", "Where", "Recording"]
        options = [name, artist, where, recording]
        final_suggestion = ""
        for i in range(len(options)):
            if not checkforbad(options[i]):
                return await ctx.response.send_message(
                    f"{ctx.author.mention}  **That word is not allowed in this server.**",
                    ephemeral=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,users=False))
        for i in range(len(options)):
            final_suggestion += f"{stuff[i]}:  {options[i]}\n"
        suggest_channel = self.bot.get_channel(815770418006196235)
        embed = discord.Embed(description=final_suggestion,color=0x89aa00,timestamp=datetime.datetime.utcnow())
        if ctx.author.guild_avatar:
            embed.set_author(name=ctx.author, icon_url=ctx.author.guild_avatar)
        else:
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.response.send_message(
            content=
            f"{ctx.author.mention} **Your song suggestion has been submitted. The admins will review and reach out to you if approved.**",
            ephemeral=True,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,users=False))
        suggest = await suggest_channel.send(content=None, embed=embed)
        await suggest.add_reaction("👍")
        await suggest.add_reaction("👎")

    @_suggest.error
    @_suggestsong.error
    @_poll.error
    @_welcome.error
    async def utils_error(self, ctx, error):
        if isinstance(error,commands.MemberNotFound):
            try:
                return await ctx.response.send_message("That member isnt in the server",ephemeral=True)
            except discord.InteractionResponded:
                pass
        else:
            print(error)


def setup(bot):
    print("Loaded Utils")
    bot.add_cog(utils(bot))
