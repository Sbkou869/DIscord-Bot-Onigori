import disnake, datetime
from disnake.ext import commands

from database.AdminsListDB import AdminListDatabase

admin_db = AdminListDatabase()

class AdminList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="admin_list", description="Администрация сервера")
    async def admins(self, interaction):
        await admin_db.create_table_admins_list()
        top = await admin_db.get_admins_sorted(interaction.guild.id)
        
        if not top:
            await interaction.response.send_message("Список администраторов пуст.", ephemeral=True)
            return
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}. {user[1]}**\n'
            if loop_count % 10 == 0 or loop_count == len(top):
                embed = disnake.Embed(color=disnake.Color.old_blurple(), title='Администрация дискорда')
                embed.description = text
                embed.timestamp = datetime.datetime.now()
                embeds.append(embed)
                text = ''
        await interaction.response.send_message(embed=embeds[0], ephemeral=True)

    @commands.slash_command(name="add_admin", description="Добавить администратора в список")
    @commands.has_permissions(administrator=True)
    async def add_admin(self, intreaction, member:disnake.Member):
        await admin_db.create_table_admins_list()
        await admin_db.insert_admins(intreaction.guild, member)
        await intreaction.response.send_message(f"Вы успешно добавили {member.name} в список администраторов.", ephemeral=True)
        
    @commands.slash_command(name="del_admin", description="Удалить администратора из списка")
    @commands.has_permissions(administrator=True)
    async def del_admin(self, interaction, member: disnake.Member):
        existing_admin = await admin_db.get_admins(member)
        if not existing_admin:
            await interaction.response.send_message(f"{member.name} не является администратором.", ephemeral=True)
            return
        
        await admin_db.remove_admin(member)
        await interaction.response.send_message(f"Вы успешно удалили {member.name} из списка администраторов.", ephemeral=True)
    
        
def setup(bot):
    bot.add_cog(AdminList(bot))