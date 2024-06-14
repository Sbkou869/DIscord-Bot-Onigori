import disnake
from disnake.ext import commands
from database.Database import UsersDataBase

db = UsersDataBase()

class Set_LogChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="Установка канала логирования")
    @commands.has_permissions(administrator=True)
    async def set_log(self, interaction: disnake.ApplicationCommandInteraction, channel_id: disnake.TextChannel):
        guild_id = interaction.guild.id
        await db.create_table_log_chanel()
        await db.insert_logs_channel(interaction, channel_id, guild_id)
        
        
def setup(bot):
    bot.add_cog(Set_LogChannel(bot))