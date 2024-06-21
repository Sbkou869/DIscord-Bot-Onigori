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
        await welcome_db.add_welcome_channel(interaction.guild, channel_id)
        
        channel = interaction.guild.get_channel(await log_db.get_log_channel(interaction.guild)) 
        await channel.send(f"Каналом приветсвия в гильдии {interaction.guild.name} был установлен {channel_id.name} администатором {interaction.author.mention}")
        
    @commands.slash_command(description="Удаление канала приветсвия")
    @commands.has_permissions(administrator=True)
    async def remove_welcome_channel(self, interaction: disnake.ApplicationCommandInteraction):
        await welcome_db.remove_channel(interaction.guild)
        channel = interaction.guild.get_channel(await log_db.get_log_channel(interaction.guild)) 
        await channel.send(f"Канал приветсвия в гильдии {interaction.guild.name} был удален администатором {interaction.author.mention}")
    
        
def setup(bot):
    bot.add_cog(Set_WelcomeChannel(bot))