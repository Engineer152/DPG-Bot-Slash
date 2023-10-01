# importing modules
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random, math
import os
from dotenv import load_dotenv
from easy_pil import Editor, load_image_async, Font, Text
import aiohttp
import dns

"""
LEVEL FORMULA FROM XP
import math
xp = 1157645 #ava's xp
math.floor(0.1*math.sqrt(xp))

---------------------------------------------------
---------------------------------------------------
GAP FORMULA 
import math
xp = 1158101 # again ava's xp
level = math.floor(0.1*math.sqrt(xp))
nxtlevel = level + 1 
xpnxtlevl = (100*nxtlevel*nxtlevel)-(100*level*level)
xpnxtlevl
"""
# https://github.com/Sitiaro/Discord.py/blob/main/levels.py
load_dotenv()
# BOT DEV SERVER STUFF
bot_channel = 756175869437018165
talk_channels = [
    756175869437018165, 756172745099706492, 836250053156405248,
    801078037768699994, 796431608655773778, 858329586625282048,
    831889081360973865
]  # ID's of every channel wherein you want the bot to allot xp to a user
levels = [5, 10, 15, 30, 40, 50, 75, 100]
level = {
    5:768193676055805962,
    10:768193781220507739,
    15:768193866003513416,
    30:768194080383041536,
    40:768194218409459723,
    50:768194316798525480,
    75:768194450618318848,
    100:768194973551820861
}
# you can have as many levels as you like
# OLD f"mongodb+srv://dpgbot:{password}@dpgbot.vo3ed.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

password = os.environ['MONGO_PASS']
cluster = MongoClient(
    f"mongodb+srv://dpgbotuser:{password}@dpgbotdb.xc0wygc.mongodb.net/?retryWrites=true&w=majority"
)
collection_name = cluster["Servers"]
print(collection_name.list_collection_names())
class levelsys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd = commands.CooldownMapping.from_cooldown(
            1.0, 120.0, commands.BucketType.member)

    def ratelimit_check(self, message):
        """Returns the ratelimit left"""
        bucket = self.cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        # if message.channel.id not in talk_channels:
        #     return
        if message.channel.id == 801469012528594944 :
            return
        if message.content.strip().count("░")>50:
            await message.reply("Please avoid spamming in the server",delete_after=5,allowed_mentions=discord.AllowedMentions.none())
            await message.delete()
            return
        retry_after = self.ratelimit_check(message)
        if not retry_after:
            
            guild_id = str(message.guild.id)
            server_cluster = collection_name[guild_id]
            stats = server_cluster.find_one({"id": message.author.id})
            if not stats:
                newuser = {
                    "id": message.author.id,
                    "user": message.author.display_name,
                    "avatar": message.author.display_avatar.url,
                    "xp": 0
                }
                server_cluster.insert_one(newuser)
            else:
                inc = random.randint(30, 50)
                xp = stats["xp"]
                server_cluster.update_one({"id": message.author.id}, {
                    "$set": {
                        "xp": xp + inc,
                        "user": message.author.display_name,
                        "avatar": message.author.display_avatar.url
                    }
                })

                lvl = math.floor(0.1 * math.sqrt(xp))
                nlvl = lvl + 1
                xpnxtlevl = (100 * nlvl * nlvl) - (100 * lvl * lvl)

                if ((xp - (100 * lvl * lvl)) + inc) >= xpnxtlevl:
                    embed = discord.Embed(
                        title="🏆 LEVEL UP! 🎉",
                        description=
                        f"Congratulations **{message.author}**!\nYou've leveled up to level **{nlvl}** 🎉 - You've made Ned proud!!",
                        color=0xd72f45)
                    embed.set_image(
                        url=
                        "https://media.giphy.com/media/3gWZiTb8Y16UyqIA80/giphy.gif"
                    )
                    if message.guild.id == 720657696407420950:
                        channel = await self.bot.fetch_channel(720657696872726530)
                    else:
                        channel = await self.bot.fetch_channel(bot_channel)
                    await channel.send(message.author.mention, embed=embed)
                    for i in message.author.roles:
                        if i.name.startswith("Level"):
                            role = int(i.name.split("Level")[-1].split("+:")[0])
                            for v in range(len(levels)):
                                if role == levels[v]:
                                    next = levels[v+1]
                            if next == nlvl :
                                for lvls in range(len(levels)):
                                    if role == levels[lvls]:
                                        toadd = levels[lvls+1]
                                await message.author.remove_roles(i, reason="Level up")
                                await message.author.add_roles(discord.Object(
                                    id=level[toadd]),reason="Level up")
                            else:
                                continue
                    if nlvl == 5:
                        await message.author.add_roles(
                            discord.Object(id=level[5]), reason="Level up")

        else:
            return

    @commands.group(aliases=['xp',"level","lvl"],
                    case_insensitive=True,
                    invoke_without_command=True)
    async def rank(self, ctx, member: discord.Member = None):
        if ctx.channel.id not in [758297067155488799,756175869437018165] :
            return
        if not member:
            member = ctx.author
        guild_id = str(ctx.guild.id)
        server_cluster = collection_name[guild_id]
        stats = server_cluster.find_one({"id": member.id})

        if not stats:
            embed = discord.Embed(
                description="You need to send messages to obtain a rank!")
            await ctx.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = math.floor(0.1 * math.sqrt(xp))
            nlvl = lvl + 1
            rank = 0
            people=[]
            for i in ctx.guild.members:
                people.append(i.display_name)
            xpnxtlvl = (100 * nlvl * nlvl) - (100 * lvl * lvl)
            rankings = server_cluster.find().sort("xp", pymongo.DESCENDING)
            for x in rankings:
                if x["user"] == "#" or not x['avatar'] or x["user"] not in people:
                    continue
                rank += 1
                if stats["id"] == x["id"]:
                    break
            # using this to send all the info
            boxes = int(
                math.floor(((xp - 100 * lvl * lvl) / xpnxtlvl) * 100) / 10)

            if f"{member.id}.png" in os.listdir(f"background/{ctx.guild.id}"):
                background = Editor(f"background/{ctx.guild.id}/{member.id}.png")
            else:
                background = Editor(f"background/{ctx.guild.id}/default.png")
            background.resize((934, 282))

            # For profile to use users profile picture load it from url using the load_image/load_image_async function
            profile_image = await load_image_async(
                str(member.display_avatar.url))
            profile = Editor(profile_image).resize((190, 190)).circle_image()

            poppins = Font.poppins(size=30, variant="bold")

            # background.rectangle((20, 20), 894, 242, "#2a2e35")
            background.paste(profile, (30, 50))
            background.ellipse((25, 42), width=206, height=206, outline=member.color.to_rgb(), stroke_width=10)
            background.rectangle((260, 180),
                                 width=630,
                                 height=40,
                                 fill="#484b4e",
                                 radius=20)
            background.bar(
                (260, 180),
                max_width=630,
                height=40,
                percentage=boxes * 10,
                fill="#33f3ff",
                radius=20,
            )
            background.text((270, 120),
                            member.display_name[:22],
                            font=poppins,
                            color="white")
            background.text(
                (870, 125),
                f"{xp - (100 * lvl * lvl)}/{xpnxtlvl}",
                font=poppins,
                color="white",
                align="right",
            )

            rank_level_texts = [
                Text("Rank ", color="white", font=poppins),
                Text(f"{rank}", color="white", font=poppins),
                Text("   Level ", color="white", font=poppins),
                Text(f"{lvl}", color="white", font=poppins),
            ]

            background.multicolor_text((850, 30),
                                       texts=rank_level_texts,
                                       align="right")
            file = discord.File(fp=background.image_bytes, filename="card.png")
            await ctx.send(file=file)
            
    @rank.error
    async def rankerror(self,ctx,error):
        print(error)
    
    @rank.command(name="set-background", aliases=["set-bg","bg-set"])
    @commands.has_any_role(778822337503690762,757760951620468817,723187777465876543,763044012755779664,768509120525107230)
    async def setbg(self, ctx, link: str = None):
        if not link and ctx.message.attachments:
            link = ctx.message.attachments[0].url
        if not link:
            return await ctx.send(
                "Please provide a link or attach an image to your message")
        async with aiohttp.ClientSession() as s:
            async with s.get(link) as r:
                if r.status == 200:
                    with open(f"background/{ctx.guild.id}/{ctx.author.id}.png",
                              mode="wb") as file:
                        file.write(await r.read())
                    await ctx.send("Background set!")
                else:
                    return await ctx.send(
                        "An error occurred\n Please contact `ironman9356#3125`"
                    )

    # Leaderboard
    @setbg.error
    async def setbgerror(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            return await ctx.send(
                "You need the `@MVP` role or above to change your background")
        print(error, type(error))

    @rank.command(name="remove-background", aliases=["remove-bg","bg-remove"])
    @commands.has_any_role(778822337503690762,757760951620468817,723187777465876543,763044012755779664,768509120525107230)
    async def rmbg(self, ctx):
        if f"{ctx.author.id}.png" in os.listdir("background"):
            os.remove(f"background/{ctx.guild.id}/{ctx.author.id}.png")
            return await ctx.send("Your BG has been set to default")
        else:
            return await ctx.send("You dont have a backgorund set")

    @rmbg.error
    async def rmbgerror(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            return await ctx.send(
                "You need the `@MVP` role or above to change your background")
        print(error, type(error))

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, page: int = 1):
        guild_id = str(ctx.guild.id)
        server_cluster = collection_name[guild_id]
        rankings = server_cluster.find().sort("xp", pymongo.DESCENDING)
        members = ctx.guild.members
        people=[]
        for i in ctx.guild.members:
            people.append(i.display_name)
        names = []
        for i in members:
            names.append(i.display_name)
        pages = page
        if page != 1:
            page = (page * 10) + 1 - 10
        embed = discord.Embed(title="🏀 Leaderboard 🏆", color=0xd72f45)
        desc = ""
        desc_list = []
        v = 1

        for i in rankings:
            if i["user"] == "#" or not i['avatar'] or i["user"] not in people:
                    continue
            tempxp = i["xp"]
            if i['user'] in names:
                try:
                    desc_list.append(
                        f"**{v}:** [{i['user']}]({i['avatar']}) :: Level {math.floor(0.1 * math.sqrt(tempxp))} ({tempxp} XP)\n"
                    )
                    v += 1
                except Exception:
                    continue
            else:
                continue
        a = 0
        for i in range(page - 1, len(desc_list)):
            if a == 10:
                break
            desc += desc_list[i]
            a = a + 1

        if not desc.strip():
            return await ctx.send("There were no users on that page!")
        embed.description = desc.strip()
        embed.set_footer(text=f"Page {pages}")
        await ctx.channel.send(embed=embed)

    @rank.error
    @leaderboard.error
    async def leveling_error(self, ctx, error):
        await ctx.send("An error has occured please try again later")

    # @commands.command()
    # async def imp(self, ctx):
    #   import json
    #   with open('./dpg_fans.json', 'r') as f:
    #     data = json.load(f)
    #     data = data['Users']
    #     guild_id = "720657696407420950"
    #     server_cluster = collection_name[guild_id]
    #     for user in data:
    #       newuser = {
    #           "id": int(user["userId"]),
    #           "user": str(user["userName"]),
    #           "avatar": "",
    #           "xp": int(user["totalXp"])
    #       }
    #       server_cluster.insert_one(newuser)

# setting up cogs
def setup(client):
    print("Loaded Leveling")
    client.add_cog(levelsys(client))
