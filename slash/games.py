import discord
from discord.ext import commands
import asyncio
import requests
import html
import random


def convert(seconds: int):
    seconds = round(seconds)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if int(hour) != 0:
        if hour <= 10 and minutes <= 10:
            return f'{hour} hour {minutes} minutes {seconds} seconds'
    elif hour == 0 and minutes != 0:
        return f'{int(minutes)} minutes {seconds} seconds'
    elif minutes == 0:
        return f'{seconds} seconds'


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


def data(category: int = None):

    x = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
    if category:
        x = requests.get(
            f"https://opentdb.com/api.php?amount=1&category={int(category) + 8}&type=multiple")
    trivia = x.json()
    question = trivia["results"][0]
    category = question["category"]
    qtype = question["difficulty"]
    q = question["question"]
    q = html.unescape(q)
    answer = question["correct_answer"]
    answer = html.unescape(answer)
    list1 = [answer]
    for i in question["incorrect_answers"]:
        list1.append(html.unescape(i))
    random.shuffle(list1)
    return dict([["question", q], ["category", category], ["qtype", qtype],
                 ["answer", answer], ["options", list1]])


class Trivia(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=15.0)
        self.value = None
        self.question = None
        self.answer = None
        self.options = None
        self.users = []
        self.click = {}

    @discord.ui.button(label=None)
    async def option1(self, button: discord.ui.Button,
                      interaction: discord.Interaction):
        self.option1.disabled = True
        self.option2.disabled = True
        self.option3.disabled = True
        self.option4.disabled = True

    @discord.ui.button(label=None)
    async def option2(self, button: discord.ui.Button,
                      interaction: discord.Interaction):
        self.option1.disabled = True
        self.option2.disabled = True
        self.option3.disabled = True
        self.option4.disabled = True

    @discord.ui.button(label=None)
    async def option3(self, button: discord.ui.Button,
                      interaction: discord.Interaction):
        self.option1.disabled = True
        self.option2.disabled = True
        self.option3.disabled = True
        self.option4.disabled = True

    @discord.ui.button(label=None)
    async def option4(self, button: discord.ui.Button,
                      interaction: discord.Interaction):
        self.option1.disabled = True
        self.option2.disabled = True
        self.option3.disabled = True
        self.option4.disabled = True

    async def interaction_check(self, interaction):
        self.value = self.answer
        if interaction.author in self.click.keys():
            self.click.update(
                {interaction.author: self.click[interaction.author] + 1})
            if interaction.component.label == self.answer and interaction.author not in self.users:
                self.users.append(interaction.author)
            if interaction.author in self.users and interaction.component.label != self.answer:
                self.users.remove(interaction.author)
            return await interaction.response.send_message(
                "Your response has been edited", ephemeral=True)
        else:
            self.click.update({interaction.author: 1})
            if interaction.component.label == self.answer:
                self.users.append(interaction.author)
            return await interaction.response.send_message(
                "Your response has been submitted", ephemeral=True)


class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="trivia",
        description="Are you bored? Lets play some trivia!",
        guild_ids=[720657696407420950])
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def _trivia(self,
                      interaction: discord.CommandInteraction,
                      topic: str = commands.Param(
                          description="Choose a specific topic!",
                          default=False)):
        if interaction.channel.id != 829319368038285322:
            return await interaction.response.send_message(
                "Wrong channel please use <#829319368038285322> for /trivia",
                ephemeral=True)
        if not topic:
            x = data()
            trivia = Trivia()
            trivia.answer = x["answer"]
            trivia.option1.label = x["options"][0]
            trivia.option2.label = x["options"][1]
            trivia.option3.label = x["options"][2]
            trivia.option4.label = x["options"][3]
            embed = discord.Embed(
                title="TRIVIA TIME!",
                description=f"Theme: {x['category'].title()}\nDifficulty: "
                f"{x['qtype'].title()}\nQuestion: **"
                f"{x['question']}**\n__**You have "
                f"15s to click/tap on the correct button**__",
                color=discord.Color.random())
            embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")
            await interaction.response.send_message(embed=embed, view=trivia)
            message = await interaction.original_message()
            await trivia.wait()
            if not trivia.value:
                trivia.option1.disabled = True
                trivia.option2.disabled = True
                trivia.option3.disabled = True
                trivia.option4.disabled = True
                embed = discord.Embed(
                    title="TRIVIA TIME!",
                    description=f"Theme: {x['category'].title()}\nDifficulty: "
                    f"{x['qtype'].title()}\nQuestion: **"
                    f"{x['question']}**\n\n**TIME UP**",
                    color=discord.Color.red())
                embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")
                await message.edit(embed=embed, view=trivia)
                embed = discord.Embed(
                    description=f"Time up!\nCorrect answer is `{trivia.answer}`\nNo one answered",
                    color=discord.Color.red())
                await message.reply(embed=embed)
                return
            trivia.option1.disabled = True
            trivia.option2.disabled = True
            trivia.option3.disabled = True
            trivia.option4.disabled = True
            correct_user = ""
            count = 0
            for i in trivia.users:
                correct_user += f"{count + 1}. <@!{i.id}>\n"
                count += 1

            if trivia.users:
                embed = discord.Embed(
                    title="TRIVIA TIME!",
                    description=f"Theme: {x['category'].title()}\nDifficulty: "
                    f"{x['qtype'].title()}\nQuestion: **"
                    f"{x['question']}**",
                    color=discord.Color.green())
                embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")

                await message.edit(embed=embed, view=trivia)
                embed = discord.Embed(
                    description=f"**Time up!**\nCorrect answer is `{trivia.answer}`\nThe people who got it correct are:\n{correct_user.strip()}",
                    color=discord.Color.green())
                await message.reply(embed=embed)

            elif not trivia.users:
                embed = discord.Embed(
                    title="TRIVIA TIME!",
                    description=f"Theme: {x['category'].title()}\nDifficulty:"
                    f" {x['qtype'].title()}\nQuestion: **"
                    f"{x['question']}**",
                    color=discord.Color.red())
                embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")

                await message.edit(embed=embed, view=trivia)
                embed = discord.Embed(
                    description=f"**Time up!**\nCorrect answer is `{trivia.answer}`\nNo one got it right",
                    color=discord.Color.red())
                await message.reply(embed=embed)

            else:
                await message.reply("error")
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
                await interaction.response.send_message(embed=embed)
            else:
                num = topic.split(".")[0]
                x = data(num)
                trivia = Trivia()
                trivia.answer = x["answer"]
                trivia.option1.label = x["options"][0]
                trivia.option2.label = x["options"][1]
                trivia.option3.label = x["options"][2]
                trivia.option4.label = x["options"][3]
                embed = discord.Embed(
                    title="TRIVIA TIME!",
                    description=f"Theme: {x['category'].title()}\nDifficulty: "
                    f"{x['qtype'].title()}\nQuestion: **"
                    f"{x['question']}**\n__**You have "
                    f"15s to click/tap on the correct button**__",
                    color=discord.Color.random())
                embed.set_thumbnail(url="https://i.ibb.co/x6dhj1m/trivia.png")
                await interaction.response.send_message(embed=embed, view=trivia)
                message = await interaction.original_message()
                await trivia.wait()
                if not trivia.value:
                    trivia.option1.disabled = True
                    trivia.option2.disabled = True
                    trivia.option3.disabled = True
                    trivia.option4.disabled = True
                    embed = discord.Embed(
                        title="TRIVIA TIME!",
                        description=f"Theme: {x['category'].title()}\nDifficulty: "
                        f"{x['qtype'].title()}\nQuestion: **"
                        f"{x['question']}**\n\n**TIME UP**",
                        color=discord.Color.red())
                    embed.set_thumbnail(
                        url="https://i.ibb.co/x6dhj1m/trivia.png")
                    await message.edit(embed=embed, view=trivia)
                    embed = discord.Embed(
                        description=f"Time up!\nCorrect answer is `{trivia.answer}`\nNo one answered",
                        color=discord.Color.red())
                    await message.reply(embed=embed)
                    return
                trivia.option1.disabled = True
                trivia.option2.disabled = True
                trivia.option3.disabled = True
                trivia.option4.disabled = True
                correct_user = ""
                count = 0
                for i in trivia.users:
                    correct_user += f"{count + 1}. <@!{i.id}>\n"
                    count += 1

                if trivia.users:
                    embed = discord.Embed(
                        title="TRIVIA TIME!",
                        description=f"Theme: {x['category'].title()}\nDifficulty: "
                        f"{x['qtype'].title()}\nQuestion: **"
                        f"{x['question']}**",
                        color=discord.Color.green())
                    embed.set_thumbnail(
                        url="https://i.ibb.co/x6dhj1m/trivia.png")

                    await message.edit(embed=embed, view=trivia)
                    embed = discord.Embed(
                        description=f"**Time up!**\nCorrect answer is `{trivia.answer}`\nThe people who got it correct are:\n{correct_user.strip()}",
                        color=discord.Color.green())
                    await message.reply(embed=embed)

                elif not trivia.users:
                    embed = discord.Embed(
                        title="TRIVIA TIME!",
                        description=f"Theme: {x['category'].title()}\nDifficulty:"
                        f" {x['qtype'].title()}\nQuestion: **"
                        f"{x['question']}**",
                        color=discord.Color.red())
                    embed.set_thumbnail(
                        url="https://i.ibb.co/x6dhj1m/trivia.png")

                    await message.edit(embed=embed, view=trivia)
                    embed = discord.Embed(
                        description=f"**Time up!**\nCorrect answer is `{trivia.answer}`\nNo one got it right",
                        color=discord.Color.red())
                    await message.reply(embed=embed)

                else:
                    await message.reply("error")

    @_trivia.autocomplete("topic")
    async def autocomp_trivia(self, interaction, user_input: str):
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

    @commands.slash_command(name="battle",
                            description="Battle your friends for the trophy!",
                            guild_ids=[720657696407420950])
    @commands.cooldown(8, 28800, commands.BucketType.member)
    async def _battle(self,
                      interaction: discord.CommandInteraction,
                      member1: discord.Member = commands.Param(
                          description="The first member", default=False),
                      member2: discord.Member = commands.Param(
                          description="The second member", default=False)):
        if interaction.channel.id != 758297067155488799:
            return await interaction.response.send_message(
                "Wrong channel\nPlease use <#758297067155488799>",
                ephemeral=True)

        member_life = 100
        user_life = 100

        user = member1
        member = member2
        if not member and not user:
            user = interaction.author
            member = self.bot.user
        if not member:
            member = member1
            user = interaction.author
        if not user:
            user = interaction.author
            member = self.bot.user

        if member.id == user.id:
            if self._battle.get_cooldown_retry_after(interaction) == 0.0:
                pass
            else:
                self._battle.reset_cooldown(interaction)
            return await interaction.response.send_message(
                "Two same people can't battle each other lol ", ephemeral=True)
        if member.bot and member != self.bot.user:
            if self._battle.get_cooldown_retry_after(interaction) == 0.0:
                pass
            else:
                self._battle.reset_cooldown(interaction)
            return await interaction.response.send_message(
                "No battling with other bots", ephemeral=True)

        if user.bot and member != self.bot.user:
            if self._battle.get_cooldown_retry_after(interaction) == 0.0:
                pass
            else:
                self._battle.reset_cooldown(interaction)
            return await interaction.response.send_message(
                "No battling with other bots", ephemeral=True)
        round = 0
        embed = discord.Embed(title=':basketball: TRICKSHOT BATTLE :football:',
                              color=0xd92c43,
                              description='*Match starting in 3...*')
        embed.add_field(name=f'{member.name}',
                        value=f'{member_life}/100',
                        inline=True)
        embed.add_field(name=f'{user.name}', value=f'{user_life}/100')
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(3)
        embed.clear_fields()
        embed1 = discord.Embed(
            title=':basketball: TRICKSHOT BATTLE :football:', color=0xd92c43)
        embed1.add_field(name=f'{member.name}',
                         value=f'{member_life}/100',
                         inline=True)

        embed1.add_field(name=f"{user.name}",
                         value=f"{user_life}/100",
                         inline=True)

        await interaction.edit_original_message(embed=embed1)
        round = round + 1
        x = rng()
        embed1.insert_field_at(
            0,
            value=f':arrow_left: **{interaction.author.name}** did a trickshot against **{member.name}**, '
            f'They scored __{x}__ points!',
            name=f"ROUND {round}",
            inline=False)
        member_life = member_life - x
        embed1.set_field_at(-2,
                            name=f'{member.name}',
                            value=f'{member_life}/100',
                            inline=True)

        await interaction.edit_original_message(embed=embed1)
        await asyncio.sleep(2)
        round = round + 1
        y = rng()
        embed1.insert_field_at(
            1,
            value=f':arrow_right: **{member.name}** did a trickshot against **{user.name}**, '
            f'They scored __{y}__ points!',
            name=f"ROUND {round}",
            inline=False)
        user_life = user_life - y
        embed1.set_field_at(-1,
                            name=f"{interaction.author.name}",
                            value=f"{user_life}/100",
                            inline=True)
        await asyncio.sleep(2)
        await interaction.edit_original_message(embed=embed1)
        round += 1
        z = rng()
        embed1.insert_field_at(
            2,
            value=f':arrow_left: **{user.name}** did a trickshot against **{member.name}**, '
            f'They scored __{z}__ points!',
            name=f"ROUND {round}",
            inline=False)
        member_life = member_life - x
        embed1.set_field_at(-2,
                            name=f'{member.name}',
                            value=f'{member_life}/100',
                            inline=True)
        await asyncio.sleep(2)
        await interaction.edit_original_message(embed=embed1)
        while member_life >= 0 or user_life >= 0:
            round += 1
            y = rng()
            embed1.remove_field(0)
            embed1.insert_field_at(
                2,
                value=f':arrow_right: **{member.name}** did a trickshot agai'
                f'nst **{user.name}**, They scored __{y}__ points!',
                name=f"ROUND {round}",
                inline=False)
            user_life = user_life - y
            if user_life <= 0:
                user_life = 0
            embed1.set_field_at(-1,
                                name=f"{user.name}",
                                value=f"{user_life}/100",
                                inline=True)
            await asyncio.sleep(2)
            await interaction.edit_original_message(embed=embed1)

            if user_life <= 0:
                embed1.remove_field(0)
                embed1.insert_field_at(
                    2,
                    value=f':trophy: **{member.name}** has won!',
                    name="WINNER",
                    inline=False)
                await interaction.edit_original_message(embed=embed1)
                break
            round += 1

            embed1.remove_field(0)
            x = rng()
            embed1.insert_field_at(
                2,
                value=f':arrow_left: **{user.name}** did a trickshot agai'
                f'nst **{member.name}**, They scored __{x}__ points!',
                name=f"ROUND {round}",
                inline=False)
            member_life = member_life - x
            if member_life <= 0:
                member_life = 0
            embed1.set_field_at(-2,
                                name=f'{member.name}',
                                value=f'{member_life}/100',
                                inline=True)
            await asyncio.sleep(2)
            await interaction.edit_original_message(embed=embed1)
            if member_life <= 0:
                embed1.remove_field(0)
                embed1.insert_field_at(
                    2,
                    value=f':trophy: **{user.name}** has won!',
                    name="WINNER",
                    inline=False)
                await interaction.edit_original_message(embed=embed1)
                break

        message = await interaction.original_message()
        # await message.add_reaction('<:GG:811602518764814376>')
        await message.add_reaction('<:GG:1002796083040231474>')

    @_trivia.error
    async def _trivia_error(self, interaction: discord.CommandInteraction, error):
        if isinstance(error, commands.CommandOnCooldown):
            try:
                await interaction.response.send_message(
                    f":warning: You Cannot play trivia for another: {convert(int(error.retry_after))}.",
                    ephemeral=True)
            except discord.InteractionResponded:
                pass
        else:
            print("error: ", error)

    @_battle.error
    async def battle_error(self, interaction: discord.CommandInteraction, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await interaction.response.send_message(
                f"{interaction.author.display_name} :warning: You cannot battle for another: {convert(int(error.retry_after))}.", ephemeral=True
            )


def setup(bot):
    print("Loaded Games")
    bot.add_cog(games(bot))
