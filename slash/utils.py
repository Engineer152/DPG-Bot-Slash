import discord
import datetime
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import pickle


client = commands.Bot(command_prefix='.', case_insensitive=True)
slash = SlashCommand(client, sync_commands=True, override_type=True, sync_on_cog_reload=True,
                     delete_from_unused_guilds=True)

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
        if bad[i] in message.split(" "):
            return False
    return True


class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="welcome",
        description="Welcome someone to the server",
        guild_ids=[720657696407420950],
        options=[
            create_option(
                name="member",
                description="Who is new here ?",
                option_type=6,
                required=False
            )
        ]
    )
    async def _welcome(self, ctx, member: discord.Member = None):
        if not member:
            embed = discord.Embed(
                description=f"**WELCOME TO {ctx.guild.name}\nCheck <#723279473960681473> "
                            f"and <#732263314461032529> to get started**\n\nWelcome **New Member**!",
                color=discord.Color.random())
            embed.set_image(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        if member:
            embed = discord.Embed(
                description=f"**WELCOME TO {ctx.guild.name}\nCheck <#723279473960681473> "
                            f"and <#732263314461032529> to get started**\n\nWelcome **{member.name}**!",
                color=discord.Color.random())
            embed.set_image(url=ctx.guild.icon_url)
            await ctx.send(content=f"{member.mention}", embed=embed)

    @cog_ext.cog_slash(
        name="poll",
        description="Ask a question to your friends",
        options=[
            create_option(
                name="question",
                description="This is the question.",
                option_type=3,
                required=True
            ),
            create_option(
                name="first",
                description="This is the 1st option",
                option_type=3,
                required=True
            ),
            create_option(
                name="second",
                description="This is the 2nd option",
                option_type=3,
                required=False
            ),
            create_option(
                name="third",
                description="This is the 3rd option",
                option_type=3,
                required=False
            ),
            create_option(
                name="fourth",
                description="This is the 4th option",
                option_type=3,
                required=False
            ),
            create_option(
                name="fifth",
                description="This is the 5th option",
                option_type=3,
                required=False
            ),
            create_option(
                name="sixth",
                description="This is the 6th option",
                option_type=3,
                required=False
            ),
            create_option(
                name="seventh",
                description="This is the 7th option",
                option_type=3,
                required=False
            ),
            create_option(
                name="eighth",
                description="This is the 8th option",
                option_type=3,
                required=False
            ),
            create_option(
                name="ninth",
                description="This is the 9th option",
                option_type=3,
                required=False
            ),
            create_option(
                name="tenth",
                description="This is the 10th option",
                option_type=3,
                required=False
            )
        ],
        guild_ids=[720657696407420950]
    )
    @commands.cooldown(1, 1800, commands.BucketType.member)
    async def _poll(self, ctx, question, **first):
        if not checkforbad(question):
            return await ctx.send(f"{ctx.author.mention}  **That word is not allowed in this server.**", hidden=True)
        options = list(first.values())
        if len(options) > 10:
            return await ctx.send("You cant have more than 10 options")
        final_options = ""
        for i in range(len(options)):
            if not checkforbad(options[i]):
                return await ctx.send(f"{ctx.author.mention}  **That word is not allowed in this server.**",
                                      hidden=True)
            if options[i] == "":
                continue
            final_options += f"{i + 1}. {options[i]}\n"

        embed = discord.Embed(title=question, description=final_options, color=0x46e2ec)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        poll_channel = self.client.get_channel(730882815381733459)
        await ctx.send(content=f"{ctx.author.mention} **Your poll has been put up.**", hidden=True)
        msg = await poll_channel.send(content=None, embed=embed)
        a = 0
        for v in range(len(options)):
            if options[v] == '':
                a += 1
                continue
            await msg.add_reaction(reactions[a])
            a += 1

        # await ctx.message.delete()

    @cog_ext.cog_slash(
        name="suggest",
        description="Suggest something to be added in the server",
        guild_ids=[720657696407420950],
        options=[
            create_option(
                name="suggestion",
                description="This is the suggestion.",
                option_type=3,
                required=True
            )
        ]
    )
    @commands.cooldown(1, 1800, commands.BucketType.member)
    async def _suggest(self, ctx, *, suggestion):
        if not checkforbad(suggestion):
            return await ctx.send(f"{ctx.author.mention}  **That word is not allowed in this server.**", hidden=True)
        suggest_channel = self.client.get_channel(725000413358587984)
        embed = discord.Embed(description=suggestion, color=0x89aa00, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(content=f"{ctx.author.mention} **Your suggestion has been submitted.**", hidden=True)
        suggest = await suggest_channel.send(content=None, embed=embed)
        await suggest.add_reaction("👍")
        await suggest.add_reaction("👎")

    @cog_ext.cog_slash(
        name="suggestsong",
        description="Suggest something to be added in the server",
        guild_ids=[720657696407420950],
        options=[
            create_option(
                name="name",
                description="Name of the song",
                option_type=3,
                required=True
            ),
            create_option(
                name="artist",
                description="Artist's name",
                option_type=3,
                required=True
            ),
            create_option(
                name="where",
                description="Name of the DP video that has the song in it",
                option_type=3,
                required=True
            ),
            create_option(
                name="recording",
                description="Link to a Video/Recording of just the song",
                option_type=3,
                required=True
            )

        ]
    )
    async def _suggestsong(self, ctx, **name):
        stuff = ["Name", "Artist", "Where", "Recording"]
        options = list(name.values())
        final_suggestion = ""
        for i in range(len(options)):
            if not checkforbad(options[i]):
                return await ctx.send(f"{ctx.author.mention}  **That word is not allowed in this server.**",
                                      hidden=True)
        for i in range(len(options)):
            final_suggestion += f"{stuff[i]}:  {options[i]}\n"
        suggest_channel = self.client.get_channel(815770418006196235)
        embed = discord.Embed(description=final_suggestion, color=0x89aa00, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(
            content=f"{ctx.author.mention} **Your song suggestion has been submitted. The admins will review and reach out to you if approved.**",
            hidden=True)
        suggest = await suggest_channel.send(content=None, embed=embed)
        await suggest.add_reaction("👍")
        await suggest.add_reaction("👎")

    @_suggest.error
    @_suggestsong.error
    @_poll.error
    @_welcome.error
    async def utils_error(self,ctx,error):
        print(error)
def setup(client):
    print("Loaded Utils")
    client.add_cog(utils(client))
