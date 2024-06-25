import disnake
from disnake.ext import commands
from database.Welcome_Channel import WelcomeChannel
from database.LogsDatabase import LogsDatabase

log_db = LogsDatabase
welcome_db = WelcomeChannel()

class Set_WelcomeChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="Установка канала приветсвия")
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, interaction: disnake.ApplicationCommandInteraction, channel_id: disnake.TextChannel):
        await welcome_db.create_table()
        await welcome_db.add_welcome_channel(channel_id, interaction.guild)
        
        await interaction.send("Установлено", ephemeral=True)
        
    @commands.slash_command(description="Удаление канала приветсвия")
    @commands.has_permissions(administrator=True)
    async def remove_welcome_channel(self, interaction: disnake.ApplicationCommandInteraction):
        await welcome_db.remove_channel(interaction.guild)
        await interaction.send("Удалено", ephemeral=True)
        
        
def setup(bot):
    bot.add_cog(Set_WelcomeChannel(bot))