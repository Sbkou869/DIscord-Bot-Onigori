import disnake
from disnake.ext import commands
from database.Welcome_Channel import WelcomeChannel
from database.LogsDatabase import LogsDatabase

log_db = LogsDatabase()
welcome_db = WelcomeChannel()

class Set_WelcomeChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(description="Установка канала приветсвия")
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, interaction: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        await welcome_db.create_table()
        await welcome_db.add_welcome_channel(channel, interaction.guild)
        
        log_channel_id = await log_db.get_log_channel(interaction.guild)
        if log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await log_channel.send(f"Каналом приветсвия в гильдии {interaction.guild.name} был установлен {channel.name} администатором {interaction.author.mention}")
        await interaction.response.send_message(f"Канал приветсвия установлен: {channel.mention}", ephemeral=True)
        
    @commands.slash_command(description="Удаление канала приветсвия")
    @commands.has_permissions(administrator=True)
    async def remove_welcome_channel(self, interaction: disnake.ApplicationCommandInteraction):
        await welcome_db.remove_channel(interaction.guild)
        
        log_channel_id = await log_db.get_log_channel(interaction.guild)
        if log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await log_channel.send(f"Канал приветсвия в гильдии {interaction.guild.name} был удален администатором {interaction.author.mention}")
        await interaction.response.send_message("Канал приветсвия удален.", ephemeral=True)
    
def setup(bot):
    bot.add_cog(Set_WelcomeChannel(bot))
