import disnake
from disnake.ext import commands
import datetime

from disnake.ui.action_row import ModalUIComponent
from disnake.utils import MISSING
from database.Database import UsersDataBase

global_db = UsersDataBase()

class ModalDeleteWarn(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        components = [
            disnake.ui.TextInput(label="Количество предупреждений", placeholder="Введите количество предупреждений", custom_id="count_warns"),
        ]

        title = f"Снятие предупреждения пользователю {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalDeleteWarn")
        
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        countDeleteWarn = interaction.text_values["count_warns"]
        
        await global_db.create_table_warns()
        result_cheak_db = await global_db.check_user_warn(interaction, self.member.id)
        
        if result_cheak_db: # Если пользователь есть в таблице тогда
            await global_db.delete_warn_user(self.member.id, countDeleteWarn)
            embed = disnake.Embed(color=0x2F3136, title="Снятие предупреждения")
            embed.description = f"{interaction.author.mention}, вы успешно сняли предупреждение пользователю {self.member.mention} " \
                                f"в количестве {countDeleteWarn}."
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            channel = interaction.guild.get_channel(1132400063851790409)  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"(Снятие предупреждения) Администратор {interaction.author.mention} снял предупреждение пользователю {self.member.mention} в количестве {countDeleteWarn}")
        else: # Если лож
            embed = disnake.Embed(color=0x2F3136, title="Пользователя не найдено!")
            embed.description = f"{interaction.author.mention}, Пользователь {self.member.mention} " \
                                f"не найден в таблице."
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class ModalWarn(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        components = [
            disnake.ui.TextInput(label="Количество предупреждений", placeholder="Введите количество предупреждений", custom_id="count_warns"),
            disnake.ui.TextInput(label="Причина предупреждения", placeholder="Введите причину предупреждения", custom_id="reason")
        ]

        title = f"Выдача предупреждения пользователю {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalWarn")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        countWarn = interaction.text_values["count_warns"]
        reason = interaction.text_values["reason"]
        
        await global_db.create_table_warns()
        result_cheak_db = await global_db.check_user_warn(interaction, self.member.id)
        
        if result_cheak_db: # Если пользователь есть в таблице тогда
            if await global_db.get_user_warn_count(self.member.id) >= 3: # Проверяем количество предупреждений и кикаем если больше или равно 3
                await self.member.kick()
                await interaction.response.send_message("Количество предупреждений пользователя было больше 3-х он был изгнан с сервера.")
                
            elif await global_db.get_user_warn_count(self.member.id) < 3: # Если меньше 3 тогда обновляем количество предупреждений
                await global_db.update_warns(interaction, self.member.id, countWarn)
                
                embed = disnake.Embed(color=0x2F3136, title="Предупреждение выдано!")
                embed.description = f"{interaction.author.mention}, Вы успешно выдали предупреждение пользователю {self.member.mention} " \
                                    f"в количестве {countWarn}"
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
                channel = interaction.guild.get_channel(await global_db.get_log_channel(interaction.guild.id))  # Вставить ID канала куда будут отправляться заявки
                await channel.send(f"(Обновление) Администратор {interaction.author.mention} выдал предупреждение пользователю {self.member.mention} в количестве {countWarn} ( по причине: {reason})")
                
                if await global_db.get_user_warn_count(self.member.id) >= 3: # Опять проверяем в случае истины кикаем
                    await self.member.kick()
                    await interaction.response.send_message("Количество предупреждений пользователя было больше 3-х он был изгнан с сервера.")
        else: # Если лож
            await global_db.create_table_warns()
            await global_db.insert_warns(interaction, self.member.id, self.member.name, countWarn)
            
            embed = disnake.Embed(color=0x2F3136, title="Предупреждение выдано!")
            embed.description = f"{interaction.author.mention}, Вы успешно выдали предупреждение пользователю {self.member.mention} " \
                                f"в количестве {countWarn}"
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            channel = interaction.guild.get_channel(await global_db.get_log_channel(interaction.guild.id))  # Вставить ID канала куда будут отправляться заявки
            await channel.send(f"Администратор {interaction.author.mention} выдал предупреждение пользователю {self.member.mention} в количестве {countWarn} ( по причине: {reason})")


class ModalReaname(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member
        
        components = [
            disnake.ui.TextInput(label="Новое имя пользователя", placeholder="Введите новое имя пользователя", custom_id="new_name"),
            disnake.ui.TextInput(label="Причина изменения", placeholder="Введите причину изменения", custom_id="reason")
        ]
        
        title = f"Изменение имени пользователя {member.name}"
        
        super().__init__(title=title, components=components, custom_id="modalReaname")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        new_name = interaction.text_values["new_name"]
        reason = interaction.text_values["reason"]
        
        await self.member.edit(nick=new_name)        
        embed = disnake.Embed(color=0x2F3136, title="Имя изменино!")
        embed.description = f"{interaction.author.mention}, Вы успешно изменили имя пользователю {self.member.mention} " \
                            f"на {new_name}"
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        channel = interaction.guild.get_channel(await global_db.get_log_channel(interaction.guild.id))  # Вставить ID канала куда будут отправляться заявки
        await channel.send(f"Администратор {interaction.author.mention} изменил имя пользователю {self.member.mention} на {new_name} ( по причине: {reason})")
        
        
class ButtonMuteViev(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        self.member = member
        super().__init__(timeout=None)

    @disnake.ui.button(label="30м", style=disnake.ButtonStyle.danger, custom_id="btMuteMinutes")
    async def btMute30(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 30 минут.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="1ч", style=disnake.ButtonStyle.danger, custom_id="btMuteOneHours")
    async def btMute1(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=1)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 1 час.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="2ч", style=disnake.ButtonStyle.danger, custom_id="btMuteTwoHours")
    async def btMute2(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=2)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 2 часа.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="4ч", style=disnake.ButtonStyle.danger, custom_id="btMuteFourHours")
    async def btMute4(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=4)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 4 часа.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="6ч", style=disnake.ButtonStyle.danger, custom_id="btMuteSixHours")
    async def btMute6(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=6)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 6 часов.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="8ч", style=disnake.ButtonStyle.danger, custom_id="btMuteEichHours")
    async def btMute8(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=8)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 8 часов.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="10ч", style=disnake.ButtonStyle.danger, custom_id="btMuteTheanHours")
    async def btMute10(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=10)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 10 часов.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="12ч", style=disnake.ButtonStyle.danger, custom_id="btMuteTvelfHours")
    async def btMute12(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        time = datetime.datetime.now() + datetime.timedelta(hours=12)
        await self.member.timeout(until=time)
        embed = disnake.Embed(
            title="Пользователь замьючен",
            description=f"Пользователь {self.member.mention} был замьючен на 12 часов.",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @disnake.ui.button(label="Размьтить", style=disnake.ButtonStyle.green, custom_id="btUnMute")
    async def btUnMute(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.member.timeout(until=None, reason=None)
        await interaction.send(f"{self.member.mention} Размьючен", ephemeral=True)
        
    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def btBack(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await interaction.response.defer()
        view = ButtonViev(self.member)
        embed = disnake.Embed(
            title="Панель управление пользователем",
            description="**Выберите дейсвие над пользователем...**",
            color=0xdede3e,
        )
        if self.member.avatar:
            embed.set_author(name=f"Профиль - {self.member.name}", icon_url=self.member.avatar.url)
        else:
            embed.set_author(name=f"Профиль - {self.member.name}", icon_url=self.member.default_avatar.url)
        await interaction.edit_original_message(embed=embed, view=view)
    
    
class ButtonViev(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        super().__init__(timeout=None)
        self.member = member

    @disnake.ui.button(label="Мут", style=disnake.ButtonStyle.danger, custom_id="btMute")
    async def btMuteAll(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        member = self.member
        view = ButtonMuteViev(member)

        embed = disnake.Embed(title="Мут",
            description=f"Выберите насколько замьютить пользователя {member.mention}",
            color=0xdede3e
        )

        if member.avatar:
            embed.set_author(name=f"Профиль - {member.name}", icon_url=member.avatar.url)
        else:
            embed.set_author(name=f"Профиль - {member.name}", icon_url=member.default_avatar.url)

        await interaction.response.edit_message(embed=embed, view=view)

    @disnake.ui.button(label="Забанить", style=disnake.ButtonStyle.danger, custom_id="btBan")
    async def btBan(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.member.ban()
        embed = disnake.Embed(
            title="Пользователь забанен",
            description=f"Пользователь {self.member.mention} был забанен.",
            color=disnake.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    
    @disnake.ui.button(label="Выдать предупреждение", style=disnake.ButtonStyle.danger, custom_id="btWarn")
    async def btSetWarn(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if not self.member:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(ModalWarn(self.member))
    
    @disnake.ui.button(label="Снять предупреждения", style=disnake.ButtonStyle.blurple, custom_id="btDeleteWarns")
    async def btDeleteWarns(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if not self.member:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(ModalDeleteWarn(self.member))
    
    @disnake.ui.button(label="Изменить имя", style=disnake.ButtonStyle.blurple, custom_id="btRename")
    async def btRename(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if not self.member:
            await interaction.response.defer()
        else:
            await interaction.response.send_modal(ModalReaname(self.member))
            
    
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="admin_help", description="Панель администратора", dm_permission=False)
    @commands.has_permissions(administrator=True)
    async def panel_admin_help(self, interaction: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Команды панели администратора",
            description="*`/mute [user] [time]` - Замьтить мользователя**\n\n"
                        "**`/unmute [user]` - Размьтить пользователя**\n\n"
                        "**`/ban` [user]` - Забанить пользователя**\n\n"
                        "**`/user_panel [user]` - Управление пользователем**\n\n",
            color=0xdede3e,
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(datetime.datetime.now())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="user", description="Управление пользователем", dm_permission=False)
    @commands.has_permissions(administrator=True)
    async def user_panel(self, interaction: disnake.ApplicationCommandInteraction, member: disnake.Member):
        view = ButtonViev(member)
        embed = disnake.Embed(
            title="Панель управление пользователем",
            description="**Выберите дейсвие над пользователем...**",
            color=0xdede3e,
        )
        if member.avatar:
            embed.set_author(name=f"Профиль - {member.name}", icon_url=member.avatar.url)
        else:
            embed.set_author(name=f"Профиль - {member.name}", icon_url=member.default_avatar.url)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(Admin(bot))