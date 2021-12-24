import discord
from discord.ext import commands
import asyncio
import requests, html
import random


def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if minutes == 0:
        return f'{seconds} seconds'
    return f'{minutes} minutes {seconds} seconds'


def rng():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    if 0 < x <= 250:
        dmg = random.randint(30, 40)
        return dmg
    elif 251 <= x <= 500:
        dmg = random.randint(20, 30)
        return dmg
    elif 501 <= x <= 750:
        dmg = random.randint(10, 20)
        return dmg
    elif x == 500 or x == 0:
        dmg = random.randint(40, 50)
        return dmg
    elif x == 1000 and y == 1000:
        dmg = 100
        return dmg
    else:
        dmg = random.randint(1, 10)
        return dmg


class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="trivia",
        description="Are you bored? Lets play some trivia!",
        guild_ids=[720657696407420950])
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def _trivia(self,
                      ctx,
                      topic: str = commands.Param(
                          description="Choose a specific topic!",
                          default=False)):
        if ctx.channel.id != 829319368038285322:
            return await ctx.response.send_message(
                "Wrong channel please use <#829319368038285322> for /trivia",
                ephemeral=True)
        if not topic:
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
                options += f"{i + 1}) {html.unescape(list1[i])}\n"
            embed = discord.Embed(
                title="TRIVIA TIME!",
                description=
                f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **"
                f"{q}**\n__**You have 15s to react with the correct emoji**__",
                color=discord.Color.random())
            embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")
            embed.add_field(name="OPTIONS", value=options, inline=False)
            await ctx.response.send_message(embed=embed)
            message = await ctx.original_message()
            reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
            for i in range(len(list1)):
                await message.add_reaction(reactions[i])

            def answer():
                for i in range(len(list1)):
                    if list1[i] == html.unescape(question["correct_answer"]):
                        return int(i)

            await asyncio.sleep(15)
            users = []
            message = self.bot.get_message(message.id)
            msg = message
            for i in message.reactions:
                useridlist = []
                reaction_list = await i.users().flatten()
                for v in reaction_list:
                    if v.id == self.bot.user.id:
                        continue
                    useridlist.append(v.id)
                users.append(useridlist)
            dict1 = {}
            for i in users:
                for v in i:
                    try:
                        dict1[str(v)] += 1
                    except KeyError:
                        dict1[str(v)] = 1
            correct_user = ""
            count = 0
            for i in dict1:
                if dict1[i] != 1:
                    continue
                elif dict1[i] == 1 and int(i) in users[answer()]:

                    correct_user += f"{count + 1}. <@!{int(i)}>"
                    count += 1
            if correct_user:
                embed = discord.Embed(
                    description=
                    f"Time up!\nCorrect answer is `{question['correct_answer']}`\nThe people who got it correct are:\n{correct_user.strip()}",
                    color=discord.Color.green())
                await message.reply(embed=embed)
                embed = msg.embeds[0]
                embed.color = discord.Color.green()
                await ctx.edit_original_message(embed=embed)
            else:
                embed = discord.Embed(
                    description=
                    f"Time up!\nCorrect answer is `{question['correct_answer']}`\nNo one got it right",
                    color=discord.Color.red())
                await message.reply(embed=embed)
                embed = msg.embeds[0]
                embed.color = discord.Color.red()
                await ctx.edit_original_message(embed=embed)
        if topic:
            if topic.lower() == "topics":
                embed = discord.Embed(title="**TRIVIA TIME!: Topics**",
                                      color=discord.Color.orange())
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
                embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")
                await ctx.response.send_message(embed=embed)
            else:
                num = topic.split(".")[0]
                x = requests.get(
                    f"https://opentdb.com/api.php?amount=1&category={int(num) + 8}"
                )
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
                    options += f"{i + 1}) {html.unescape(list1[i])}\n"
                embed = discord.Embed(
                    title="TRIVIA TIME!",
                    description=
                    f"Theme: {category.title()}\nDifficulty: {qtype.title()}\nQuestion: **"
                    f"{q}**\n__**You have 15s to react with the correct emoji**__",
                    color=discord.Color.random())
                embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")
                embed.add_field(name="OPTIONS", value=options, inline=False)
                await ctx.response.send_message(embed=embed)
                message = await ctx.original_message()
                reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
                for i in range(len(list1)):
                    await message.add_reaction(reactions[i])

                def answer():
                    for i in range(len(list1)):
                        if list1[i] == html.unescape(
                                question["correct_answer"]):
                            return int(i)

                await asyncio.sleep(15)
                users = []
                message = self.bot.get_message(message.id)
                msg = message
                for i in message.reactions:
                    useridlist = []
                    reaction_list = await i.users().flatten()
                    for v in reaction_list:
                        if v.id == self.bot.user.id:
                            continue
                        useridlist.append(v.id)
                    users.append(useridlist)
                dict1 = {}
                for i in users:
                    for v in i:
                        try:
                            dict1[str(v)] += 1
                        except KeyError:
                            dict1[str(v)] = 1
                correct_user = ""
                count = 0
                for i in dict1:
                    if dict1[i] != 1:
                        continue
                    elif dict1[i] == 1 and int(i) in users[answer()]:
                        correct_user += f"{count + 1}. <@!{int(i)}>"
                        count += 1
                if correct_user:
                    embed = discord.Embed(
                        description=
                        f"Time up!\nCorrect answer is `{question['correct_answer']}`\nThe people who got it correct are:\n{correct_user.strip()}",
                        color=discord.Color.green())
                    await message.reply(embed=embed)
                    embed = msg.embeds[0]
                    embed.color = discord.Color.green()
                    await ctx.edit_original_message(embed=embed)
                else:
                    embed = discord.Embed(
                        description=
                        f"Time up!\nCorrect answer is `{question['correct_answer']}`\nNo one got it right",
                        color=discord.Color.red())
                    await message.reply(embed=embed)
                    embed = msg.embeds[0]
                    embed.color = discord.Color.red()
                    await ctx.edit_original_message(embed=embed)

    @_trivia.autocomplete("topic")
    async def autocomp_trivia(self, ctx, user_input: str):
        topics = [
            "Topics", "1. General Knowledge", "2. Books", "3. Film",
            "4. Music", "5. Musicals & Theatres", "6. Television",
            "7. Video Games", "8. Board Games", "9. Science & Nature",
            "10. Computers", "11. Mathematics", "12. Mythology", "13. Sports",
            "14. Geography", "15. History", "16. Politics", "17. Art",
            "18. Celebrities", "19. Animals", "20. Vehicles", "21. Comics",
            "22. Gadget", "23. Japanese Anime & Manga",
            "24. Cartoon & Animations"
        ]
        return [topic for topic in topics if user_input in topic.lower()]

    @commands.slash_command(name="battle", description="Battle your friends for the trophy!",
                            guild_ids=[720657696407420950])
    @commands.cooldown(8, 28800, commands.BucketType.member)
    async def _battle(self, ctx,
                      member1: discord.Member = commands.Param(description="The first member", default=False),
                      member2: discord.Member = commands.Param(description="The second member", default=False)):
        if ctx.channel.id != 758297067155488799:
            return await ctx.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)

        member_life = 100
        user_life = 100

        user = member1
        member = member2
        if not member and not user:
            user = ctx.author
            member = self.bot.user
        if not member:
            member = member1
            user = ctx.author
        if not user:
            user = ctx.author
            member = self.bot.user

        if member.id == user.id:
            if self._battle.get_cooldown_retry_after(ctx) == 0.0:
                pass
            else:
                self._battle.reset_cooldown(ctx)
            return await ctx.response.send_message("Two same people can't battle each other lol ", ephemeral=True)
        if member.bot and member != self.bot.user:
            if self._battle.get_cooldown_retry_after(ctx) == 0.0:
                pass
            else:
                self._battle.reset_cooldown(ctx)
            return await ctx.response.send_message("No battling with other bots", ephemeral=True)

        if user.bot and member != self.bot.user:
            if self._battle.get_cooldown_retry_after(ctx) == 0.0:
                pass
            else:
                self._battle.reset_cooldown(ctx)
            return await ctx.response.send_message("No battling with other bots", ephemeral=True)
        round = 0
        embed = discord.Embed(title=':basketball: TRICKSHOT BATTLE :football:', color=0xd92c43,
                              description='*Match starting in 3...*')
        embed.add_field(name=f'{member.name}', value=f'{member_life}/100', inline=True)
        embed.add_field(name=f'{user.name}', value=f'{user_life}/100')
        await ctx.response.send_message(embed=embed)
        await asyncio.sleep(3)
        embed.clear_fields()
        embed1 = discord.Embed(title=':basketball: TRICKSHOT BATTLE :football:', color=0xd92c43)
        embed1.add_field(name=f'{member.name}', value=f'{member_life}/100', inline=True)

        embed1.add_field(name=f"{user.name}", value=f"{user_life}/100", inline=True)

        await ctx.edit_original_message(embed=embed1)
        round = round + 1
        x = rng()
        embed1.insert_field_at(0,
                               value=f':arrow_left: **{ctx.author.name}** did a trickshot against **{member.name}**, '
                                     f'They scored __{x}__ points!',
                               name=f"ROUND {round}", inline=False)
        member_life = member_life - x
        embed1.set_field_at(-2, name=f'{member.name}', value=f'{member_life}/100', inline=True)

        await ctx.edit_original_message(embed=embed1)
        await asyncio.sleep(2)
        round = round + 1
        y = rng()
        embed1.insert_field_at(1,
                               value=f':arrow_right: **{member.name}** did a trickshot against **{user.name}**, '
                                     f'They scored __{y}__ points!',
                               name=f"ROUND {round}", inline=False)
        user_life = user_life - y
        embed1.set_field_at(-1, name=f"{ctx.author.name}", value=f"{user_life}/100", inline=True)
        await asyncio.sleep(2)
        await ctx.edit_original_message(embed=embed1)
        round += 1
        z = rng()
        embed1.insert_field_at(2,
                               value=f':arrow_left: **{user.name}** did a trickshot against **{member.name}**, '
                                     f'They scored __{z}__ points!',
                               name=f"ROUND {round}", inline=False)
        member_life = member_life - x
        embed1.set_field_at(-2, name=f'{member.name}', value=f'{member_life}/100', inline=True)
        await asyncio.sleep(2)
        await ctx.edit_original_message(embed=embed1)
        while member_life >= 0 or user_life >= 0:
            round += 1
            y = rng()
            embed1.remove_field(0)
            embed1.insert_field_at(2,
                                   value=f':arrow_right: **{member.name}** did a trickshot agai'
                                         f'nst **{user.name}**, They scored __{y}__ points!',
                                   name=f"ROUND {round}", inline=False)
            user_life = user_life - y
            if user_life <= 0:
                user_life = 0
            embed1.set_field_at(-1, name=f"{user.name}", value=f"{user_life}/100", inline=True)
            await asyncio.sleep(2)
            await ctx.edit_original_message(embed=embed1)

            if user_life <= 0:
                embed1.remove_field(0)
                embed1.insert_field_at(2,
                                       value=f':trophy: **{member.name}** has won!',
                                       name="WINNER", inline=False)
                await ctx.edit_original_message(embed=embed1)
                break
            round += 1

            embed1.remove_field(0)
            x = rng()
            embed1.insert_field_at(2,
                                   value=f':arrow_left: **{user.name}** did a trickshot agai'
                                         f'nst **{member.name}**, They scored __{x}__ points!',
                                   name=f"ROUND {round}", inline=False)
            member_life = member_life - x
            if member_life <= 0:
                member_life = 0
            embed1.set_field_at(-2, name=f'{member.name}', value=f'{member_life}/100', inline=True)
            await asyncio.sleep(2)
            await ctx.edit_original_message(embed=embed1)
            if member_life <= 0:
                embed1.remove_field(0)
                embed1.insert_field_at(2,
                                       value=f':trophy: **{user.name}** has won!',
                                       name="WINNER", inline=False)
                await ctx.edit_original_message(embed=embed1)
                break

        message = await ctx.original_message()
        await message.add_reaction('<:GG:811602518764814376>')

    @_trivia.error
    async def _trivia_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            try:
                await ctx.response.send_message(
                    f":warning: You Cannot play trivia for another: {convert(int(error.retry_after))}.",
                    ephemeral=True)
            except discord.InteractionResponded:
                pass
        else:
            print("error: ", error)

    @_battle.error
    async def battle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.response.send_message(
                f"{ctx.author.display_name} :warning: You cannot battle for another: {convert(int(error.retry_after))}.")


def setup(bot):
    print("Loaded Games")
    bot.add_cog(games(bot))
