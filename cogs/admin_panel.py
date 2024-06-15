import disnake
from disnake.ext import commands
import datetime

# region ButtonsMutes
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

    @disnake.ui.button(label="Мут", style=disnake.ButtonStyle.blurple, custom_id="btMute")
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

    @disnake.ui.button(label="Забанить", style=disnake.ButtonStyle.blurple, custom_id="btBan")
    async def btBan(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        await self.member.ban()
        embed = disnake.Embed(
            title="Пользователь забанен",
            description=f"Пользователь {self.member.mention} был забанен.",
            color=disnake.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

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