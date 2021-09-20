import discord
from discord.ext import commands
import asyncio
import requests, html
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

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


class games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_subcommand(
        base="trivia",
        name="question",
        description="Are you bored? Lets play some trivia!",
        guild_ids=[720657696407420950]
    )
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def _question(self, ctx):
        if ctx.channel.id !=829319368038285322:
            return await ctx.send("Wrong channel please use <#829319368038285322> for /trivia",hidden=True)
        x = requests.get("https://opentdb.com/api.php?amount=1")
        trivia = x.json()
        question = trivia["results"][0]
        category = question["category"]
        qtype = question["difficulty"]
        q = question["question"]
        list1 = [question["correct_answer"]]
        for i in question["incorrect_answers"]:
            list1.append(i)
        q = html.unescape(q)
        options = ""
        random.shuffle(list1)
        for i in range(len(list1)):
            options += f"{i + 1}. {html.unescape(list1[i])}\n"
        embed = discord.Embed(title="TRIVIA TIME!",
                              description=f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **{q}**\n__**You have 15s to react with the correct emoji**__",
                              color=discord.Color.random())
        embed.set_thumbnail(
            url="https://i.ibb.co/x6dhj1m/trivia.png")
        embed.add_field(name="OPTIONS", value=options, inline=False)
        message = await ctx.send(embed=embed)
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        for i in range(len(list1)):
            await message.add_reaction(reactions[i])

        def answer():
            for i in range(len(list1)):
                if list1[i] == html.unescape(question["correct_answer"]):
                    return int(i)

        await asyncio.sleep(15)

        new_message = await ctx.channel.fetch_message(message.id)
        users = await new_message.reactions[answer()].users().flatten()
        count = 1
        correct_user = ""
        for i in users:
            if i.id == self.client.user.id:
                continue
            if i:
                correct_user += f"{count}. {i.name}\n"
                count += 1
        if correct_user:
            embed = discord.Embed(title="TRIVIA TIME!",
                                  description=f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **{q}**\n__**You have 15s to react with the correct emoji**__",
                                  color=discord.Color.green())
            embed.set_thumbnail(
                url="https://i.ibb.co/x6dhj1m/trivia.png")
            embed.add_field(name="OPTIONS", value=options, inline=False)
            await message.edit(embed=embed)
            embed = discord.Embed(
                description=f"Time up!\nCorrect answer is `{question['correct_answer']}`\nThe people who got it correct are:\n{correct_user.strip()}",
                color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="TRIVIA TIME!",
                                  description=f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **{q}**\n__**You have 15s to react with the correct emoji**__",
                                  color=discord.Color.red())
            embed.set_thumbnail(
                url="https://i.ibb.co/x6dhj1m/trivia.png")
            embed.add_field(name="OPTIONS", value=options, inline=False)
            await message.edit(embed=embed)
            embed = discord.Embed(
                description=f"Time up!\nCorrect answer is `{question['correct_answer']}`\nNo one got it right",
                color=discord.Color.red())
            await ctx.send(embed=embed)


    @cog_ext.cog_subcommand(
        base="trivia",
        name="topic",
        description="Are you bored? Lets play some trivia!",

        guild_ids=[720657696407420950],
        options=[
            create_option(
                name="topic",
                description="Choose the topic",
                option_type=3,
                required=False,
                choices=[
                    create_choice(
                        name="1. General Knowledge",
                        value="1"
                    ),
                    create_choice(
                        name="2. Books",
                        value="2"
                    ),
                    create_choice(
                        name="3. Film",
                        value="3"
                    ),
                    create_choice(
                        name="4. Music",
                        value="4"
                    ),
                    create_choice(
                        name="5. Musicals & Theatres",
                        value="5"
                    ),
                    create_choice(
                        name="6. Television",
                        value="6"
                    ),
                    create_choice(
                        name="7. Video Games",
                        value="7"
                    ),
                    create_choice(
                        name="8. Board Games",
                        value="8"
                    ),
                    create_choice(
                        name="9. Science & Nature",
                        value="9"
                    ),
                    create_choice(
                        name="10. Computers",
                        value="10"
                    ),
                    create_choice(
                        name="11. Mathematics",
                        value="11"
                    ),
                    create_choice(
                        name="12. Mythology",
                        value="12"
                    ),
                    create_choice(
                        name="13. Sports",
                        value="13"
                    ),
                    create_choice(
                        name="14. Geography",
                        value="14"
                    ),
                    create_choice(
                        name="15. History",
                        value="15"
                    ),
                    create_choice(
                        name="16. Politics",
                        value="16"
                    ),
                    create_choice(
                        name="17. Art",
                        value="17"
                    ),
                    create_choice(
                        name="18. Celebrities",
                        value="18"
                    ),
                    create_choice(
                        name="19. Animals",
                        value="19"
                    ),
                    create_choice(
                        name="20. Vehicles",
                        value="20"
                    ),
                    create_choice(
                        name="21. Comics",
                        value="21"
                    ),
                    create_choice(
                        name="22. Gadget",
                        value="22"
                    ),
                    create_choice(
                        name="23. Japanese Anime & Manga",
                        value="23"
                    ),
                    create_choice(
                        name="24. Cartoon & Animations",
                        value="24"
                    )

                ]
            )
        ]
    )
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def _topics(self, ctx, topic: str = None):
        if ctx.channel.id !=829319368038285322:
            return await ctx.send("Wrong channel please use <#829319368038285322> for /trivia",hidden=True)
        if not topic:
            embed = discord.Embed(title="**TRIVIA TIME!: Topics**", color=discord.Color.orange())
            embed.add_field(name="\u200b",
                            value="""
                            1. General Knowledge
                            2. Entertainment: Books
                            3. Entertainment: Film
                            4. Entertainment: Music
                            5. Entertainment: Musicals & Theatres
                            6. Entertainment: Television
                            7. Video Games
                            8. Board Games
                            9. Science & Nature
                            10. Science: Computers
                            11. Science: Mathematics
                            12. Mythology
                            """)
            embed.add_field(name="\u200b",
                            value="""
                            13. Sports
                            14. Geography
                            15. History
                            16. Politics
                            17. Art
                            18. Celebrities
                            19. Animals
                            20. Vehicles
                            21. Entertainment: Comics
                            22. Science: Gadget
                            23. Entertainment: Japanese Anime & Manga
                            24. Entertainment: Cartoon & Animations
                            """)
            embed.set_thumbnail(
                url="https://i.ibb.co/x6dhj1m/trivia.png")
            await ctx.send(embed=embed)
            # print(slash.subcommand)
            self._topics.reset_cooldown(ctx)
            return

        x = requests.get(f"https://opentdb.com/api.php?amount=1&category={int(topic) + 8}")
        trivia = x.json()
        question = trivia["results"][0]
        category = question["category"]
        qtype = question["difficulty"]
        q = question["question"]
        list1 = [question["correct_answer"]]
        for i in question["incorrect_answers"]:
            list1.append(i)
        q = html.unescape(q)
        options = ""
        random.shuffle(list1)
        for i in range(len(list1)):
            options += f"{i + 1}. {html.unescape(list1[i])}\n"
        embed = discord.Embed(title="TRIVIA TIME!",
                              description=f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **{q}**\n__**You have 15s to react with the correct emoji**__",
                              color=discord.Color.random())
        embed.set_thumbnail(
            url="https://i.ibb.co/x6dhj1m/trivia.png")
        embed.add_field(name="OPTIONS", value=options, inline=False)
        message = await ctx.send(embed=embed)
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        for i in range(len(list1)):
            await message.add_reaction(reactions[i])

        def answer():
            for i in range(len(list1)):
                if list1[i] == html.unescape(question["correct_answer"]):
                    return int(i)

        await asyncio.sleep(15)

        new_message = await ctx.channel.fetch_message(message.id)
        users = await new_message.reactions[answer()].users().flatten()
        count = 1
        correct_user = ""
        for i in users:
            if i.id == self.client.user.id:
                continue
            if i:
                correct_user += f"{count}. {i.name}\n"
                count += 1
        if correct_user:
            embed = discord.Embed(title="TRIVIA TIME!",
                                  description=f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **{q}**\n__**You have 15s to react with the correct emoji**__",
                                  color=discord.Color.green())
            embed.set_thumbnail(
                url="https://i.ibb.co/x6dhj1m/trivia.png")
            embed.add_field(name="OPTIONS", value=options, inline=False)
            await message.edit(embed=embed)
            embed = discord.Embed(
                description=f"Time up!\nCorrect answer is `{question['correct_answer']}`\nThe people who got it correct are:\n{correct_user.strip()}",
                color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="TRIVIA TIME!",
                                  description=f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **{q}**\n__**You have 15s to react with the correct emoji**__",
                                  color=discord.Color.red())
            embed.set_thumbnail(
                url="https://i.ibb.co/x6dhj1m/trivia.png")
            embed.add_field(name="OPTIONS", value=options, inline=False)
            await message.edit(embed=embed)
            embed = discord.Embed(
                description=f"Time up!\nCorrect answer is `{question['correct_answer']}`\nNo one got it right",
                color=discord.Color.red())
            await ctx.send(embed=embed)


    @_question.error
    @_topics.error
    async def _trivia_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":warning: You Cannot play trivia for another: {convert(int(error.retry_after))}.",
                           hidden=True)
        else:
            print("error: ", error)


def setup(client):
    print("Loaded Games")
    client.add_cog(games(client))