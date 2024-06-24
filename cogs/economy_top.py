import disnake
import datetime
from disnake.ext import commands
from database.RankDatabase import RankDatabase

RANG_DB = RankDatabase()


class PaginatorView(disnake.ui.View):
    def __init__(self, embeds, author, footer: bool, timeout=30.0):
        self.embeds = embeds  # Список эмбедов для отображения.
        self.author = author  # Автор сообщения.
        self.footer = footer  # Флаг для отображения подвала с номером страницы.
        self.timeout = timeout  # Время ожидания в секундах для автоматической очистки интерфейса.
        self.page = 0  # Текущая страница (индекс) из списка эмбедов.
        super().__init__(timeout=self.timeout)

        # Если флаг footer установлен, то добавляем номер страницы в подвал каждого эмбеда.
        if self.footer:
            for emb in self.embeds:
                emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1} из {len(self.embeds)}')

    # Создаем кнопку "Назад" со стрелкой влево.
    @disnake.ui.button(emoji= '<:GoBack:1254674151478657126>', style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        # Проверяем, что автор кнопки совпадает с автором интерфейса.
        if self.author.id == interaction.author.id:
            if self.page == 0:  # Если текущая страница - первая, перейдем на последнюю.
                self.page = len(self.embeds) - 1
            else:
                self.page -= 1  # В противном случае перейдем на предыдущую страницу.
        else:
            return

        await self.button_callback(interaction)

    # Создаем кнопку "Вперед" со стрелкой вправо.
    @disnake.ui.button(emoji='<:CircledRight:1254674149863854090>', style=disnake.ButtonStyle.grey)
    async def next(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        # Проверяем, что автор кнопки совпадает с автором интерфейса.
        if self.author.id == interaction.author.id:
            if self.page == len(self.embeds) - 1:  # Если текущая страница - последняя, перейдем на первую.
                self.page = 0
            else:
                self.page += 1  # В противном случае перейдем на следующую страницу.
        else:
            return

        await self.button_callback(interaction)

    # Обработчик нажатия кнопки, который отображает соответствующий эмбед.
    async def button_callback(self, interaction):
        # Проверяем, что автор кнопки совпадает с автором интерфейса.
        if self.author.id == interaction.author.id:
            await interaction.response.edit_message(embed=self.embeds[self.page])
        else:
            return await interaction.response.send_message('Вы не можете использовать эту кнопку!', ephemeral=True)


class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="top", description="Топ по монетам")
    async def top(self, interaction):
        pass

    @top.sub_command(name="money", description="Топ по монетам")
    async def money(self, interaction):
        top = await RANG_DB.get_top_money()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}. {self.bot.get_user(user[0])} - {user[5]} <:Coin:1251937857782808586>**\n'
            if loop_count % 10 == 0 or loop_count == len(top):
                embed = disnake.Embed(color=disnake.Color.old_blurple(), title='Топ пользователей по монетам')
                embed.description = text
                embed.timestamp = datetime.datetime.now()
                embeds.append(embed)
                text = ''
        view = PaginatorView(embeds, interaction.user, True)
        await interaction.response.send_message(embed=embeds[0], view=view)

    @top.sub_command(name="ruby", description="Топ по рубинам")
    async def ruby(self, interaction):
        top = await RANG_DB.get_top_ruby()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}. {self.bot.get_user(user[0])} - {user[6]} <:Ruby:1251937860672684163>**\n'
            if loop_count % 10 == 0 or loop_count == len(top):
                embed = disnake.Embed(color=disnake.Color.old_blurple(), title='Топ пользователей по рубинам')
                embed.description = text
                embed.timestamp = datetime.datetime.now()
                embeds.append(embed)
                text = ''
        view = PaginatorView(embeds, interaction.user, True)
        await interaction.response.send_message(embed=embeds[0], view=view)

    @top.sub_command(name="score", description="Топ по опыту")
    async def score(self, interaction):
        top = await RANG_DB.get_top_score()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}. {self.bot.get_user(user[0])} - {user[3]} <:GlowingStar:1251937859263402145>**\n'
            if loop_count % 10 == 0 or loop_count == len(top):
                embed = disnake.Embed(color=disnake.Color.old_blurple(), title='Топ пользователей по опыту')
                embed.description = text
                embed.timestamp = datetime.datetime.now()
                embeds.append(embed)
                text = ''
        view = PaginatorView(embeds, interaction.user, True)
        await interaction.response.send_message(embed=embeds[0], view=view)

def setup(bot):
    bot.add_cog(Top(bot))