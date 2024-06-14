import disnake
import os
from disnake.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command()
    async def reload(self, interaction):
        if interaction.author.id == 914812102768734258:
            for file in os.listdir("./cogs"):
                if file.endswith(".py"):
                   cog_name = file[:-3]
                   interaction.bot.unload_extension(f"cogs.{cog_name}")
                   interaction.bot.load_extension(f"cogs.{cog_name}")
            await interaction.send("Cogs rebooted!")
        else:
            await interaction.send("You have no rights to execute this team.")
                
def setup(bot):
    bot.add_cog(Reload(bot))
