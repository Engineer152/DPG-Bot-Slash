import discord
import datetime
from discord.ext import commands
import time
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
                       interaction: discord.CommandInteraction,
                       member: discord.Member = commands.Param(
                           description="Who is new here", default=False)):
        if not member:
            embed = discord.Embed(
                description=f"**WELCOME TO {interaction.guild.name}\nCheck <#723279473960681473> "
                f"and <#732263314461032529> to get started**\n\nWelcome **New Member**!",
                color=discord.Color.random())
            try:
                embed.set_image(url=interaction.guild.icon)
            except Exception:
                pass
            await interaction.response.send_message(embed=embed)
        if member:
            embed = discord.Embed(
                description=f"**WELCOME TO {interaction.guild.name}\nCheck <#723279473960681473> "
                f"and <#732263314461032529> to get started**\n\nWelcome **{member.name}**!",
                color=discord.Color.random())
            try:
                embed.set_image(url=interaction.guild.icon)
            except Exception:
                pass
            await interaction.response.send_message(content=f"{member.mention}",
                                                    embed=embed)

    @_welcome.error
    async def utils_error(self, interaction: discord.CommandInteraction, error):
        if isinstance(error, commands.MemberNotFound):
            try:
                return await interaction.response.send_message("That member isnt in the server", ephemeral=True)
            except discord.InteractionResponded:
                pass
        else:
            print(error)

    @commands.slash_command(name="ping", description="Pong!", guild_ids=[720657696407420950])
    async def _ping(self, interaction: discord.CommandInteraction):
        if interaction.channel.id != 758297067155488799:
            return await interaction.response.send_message("Wrong channel\nPlease use <#758297067155488799>", ephemeral=True)
        start = time.perf_counter()
        await interaction.response.send_message("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await interaction.edit_original_message(content=f'Pong!🏓 {round(duration,2)} ms\nWebsocket latency {round(self.bot.latency * 1000,2)} ms')


def setup(bot):
    print("Loaded Utils")
    bot.add_cog(utils(bot))
