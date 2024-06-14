import disnake

from disnake.ext import commands
from database.Database import UsersDataBase

global_db = UsersDataBase()

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="create table")
    async def crt(self, interaction):
        await global_db.create_table()
        await interaction.send("okay")
        
class Input(commands.Cog):
    def __init__(self, bot):
            self.bot = bot
            self.db = global_db
            pass

def setup(bot):
    bot.add_cog(Test(bot)) 
  
