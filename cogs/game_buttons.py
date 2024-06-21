import disnake
import datetime
import random
from database.RankDatabase import RankDatabase

global_db = RankDatabase()
TIME = datetime.datetime.now


class CostiModalMoney(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        self.member = member

        components = [
            disnake.ui.TextInput(label="Ставка в монетах", placeholder="Введите количество монет на ставку",
                                 custom_id="stavka_money"),
        ]

        title = f"{member.name}"

        super().__init__(title=title, components=components, custom_id="modalStavkaMoney")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        stavka_money = interaction.text_values["stavka_money"]
        try:
            stavka = int(stavka_money)
            curentMoney = await global_db.get_coins(self.member)

            if stavka > curentMoney:
                await interaction.response.send_message("У вас недостаточно монет для ставки.")
            else:
                num_user_first = int(random.choice('123456'))
                num_user_last = int(random.choice('123456'))
                user_sum = num_user_first + num_user_last

                num_bot_first = int(random.choice('123456'))
                num_bot_last = int(random.choice('123456'))
                bot_sum = num_bot_first + num_bot_last

                if user_sum > bot_sum:
                    await global_db.stavka_increment(self.member.id, stavka )
                    embed = disnake.Embed(
                        title="Вы выиграли!",
                        description=f"**Поздравляю вы выиграли - `{stavka}`**",
                        colour=disnake.Color.green()
                    )

                    if self.member.avatar:
                        embed.set_thumbnail(url=self.member.avatar.url)
                    else:
                        embed.set_thumbnail(url=self.member.default_avatar.url)

                    embed.add_field(name="Ваша сумма очков:", value=f"```{user_sum}```")
                    embed.add_field(name="Сумма очков бота:", value=f"```{bot_sum}```")

                    await interaction.response.send_message(embed = embed)

                elif user_sum == bot_sum:
                    embed = disnake.Embed(
                        title="Ничья!",
                        description=f"**Ничья ваши деньги были сохранены.**",
                        colour=disnake.Color.yellow()
                    )

                    if self.member.avatar:
                        embed.set_thumbnail(url=self.member.avatar.url)
                    else:
                        embed.set_thumbnail(url=self.member.default_avatar.url)

                    await interaction.response.send_message(embed=embed)
                else:
                    await global_db.stavka_dekrement(self.member.id, stavka)
                    embed = disnake.Embed(
                        title="Вы поиграли!",
                        description=f"**Увы вы проиграли -  `{stavka}`**",
                        colour=disnake.Color.red()
                    )

                    if self.member.avatar:
                        embed.set_thumbnail(url=self.member.avatar.url)
                    else:
                        embed.set_thumbnail(url=self.member.default_avatar.url)

                    embed.add_field(name="Ваша сумма очков:", value=f"```{user_sum}```")
                    embed.add_field(name="Сумма очков бота:", value=f"```{bot_sum}```")

                    await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")


class CostiButtons(disnake.ui.View):
    def __init__(self, member: disnake.Member, global_db):
        super().__init__(timeout=None)
        self.member = member
        self.global_db = global_db

    @disnake.ui.button(label="Сделать ставку за монеты", style=disnake.ButtonStyle.blurple)
    async def btMoneyStavka(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(CostiModalMoney(self.member))
        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")

    @disnake.ui.button(label="Ва-банк", style=disnake.ButtonStyle.blurple)
    async def btVabank(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            if not self.member:
                await interaction.response.defer()
            else:
                try:
                    curent_money = await global_db.get_coins(self.member)
                    num_user_first = int(random.choice('123456'))
                    num_user_last = int(random.choice('123456'))
                    user_sum = num_user_first + num_user_last

                    num_bot_first = int(random.choice('123456'))
                    num_bot_last = int(random.choice('123456'))
                    bot_sum = num_bot_first + num_bot_last

                    if user_sum > bot_sum:
                        await global_db.stavka_vabank(self.member.id, curent_money)
                        embed = disnake.Embed(
                            title="Вы выиграли!",
                            description=f"**Поздравляю вы выиграли - `{curent_money}`**",
                            colour=disnake.Color.green()
                        )

                        if self.member.avatar:
                            embed.set_thumbnail(url=self.member.avatar.url)
                        else:
                            embed.set_thumbnail(url=self.member.default_avatar.url)

                        embed.add_field(name="Ваша сумма очков:", value=f"```{user_sum}```")
                        embed.add_field(name="Сумма очков бота:", value=f"```{bot_sum}```")

                        await interaction.response.send_message(embed=embed)

                    elif user_sum == bot_sum:
                        embed = disnake.Embed(
                            title="Ничья!",
                            description=f"**Ничья ваши деньги были сохранены.**",
                            colour=disnake.Color.yellow()
                        )

                        if self.member.avatar:
                            embed.set_thumbnail(url=self.member.avatar.url)
                        else:
                            embed.set_thumbnail(url=self.member.default_avatar.url)

                        await interaction.response.send_message(embed=embed)
                    else:
                        await global_db.stavka_dekrement(self.member.id, curent_money)
                        embed = disnake.Embed(
                            title="Вы поиграли!",
                            description=f"**Увы вы проиграли -  `{curent_money}`**",
                            colour=disnake.Color.red()
                        )

                        if self.member.avatar:
                            embed.set_thumbnail(url=self.member.avatar.url)
                        else:
                            embed.set_thumbnail(url=self.member.default_avatar.url)

                        embed.add_field(name="Ваша сумма очков:", value=f"```{user_sum}```")
                        embed.add_field(name="Сумма очков бота:", value=f"```{bot_sum}```")

                        await interaction.response.send_message(embed=embed)
                except Exception as e:
                    await interaction.response.send_message(f"Ошибка: {e}")

        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.gray)
    async def btBack(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        try:
            view = GameButtons(self.member, self.global_db)
            await interaction.response.defer()

            embed = disnake.Embed(
                title="Игры",
                description="**В данном разделе вы можете выбрать, во что сыграть:**\n\n",
                color=disnake.Color.red()
            )
            embed.set_thumbnail(url=interaction.user.avatar.url)

            await interaction.edit_original_message(embed=embed, view=view, attachments=[])

        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")


class GameButtons(disnake.ui.View):
    def __init__(self, member: disnake.Member, global_db):
        super().__init__(timeout=None)
        self.member = member
        self.global_db = global_db

    @disnake.ui.button(label="Кости", style=disnake.ButtonStyle.green)
    async def btroulette(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            member = self.member
            user = await self.global_db.get_user(member)

            view = CostiButtons(member, self.global_db)

            embed = disnake.Embed(
                title="Кости",
                description=(
                    "**Участники бросают кости и делают ставки на исход этого броска.**\n"
                    "**Победитель определяется в зависимости от комбинации результатов на выпавших костях.**\n"
                ),
                color=disnake.Color.red(),
            )

            embed.add_field(name='<:Coin:1251937857782808586> Деньги', value=f'```{user[5]}```')
            embed.add_field(name='<:Ruby:1251937860672684163> Рубины', value=f'```{user[6]}```')

            embed.set_image(file=disnake.File("image/icons/Kosti.jpg"))  # Убедитесь, что путь к изображению корректный

            await interaction.response.edit_message(embed=embed, view=view)

        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")


def setup(bot):
    pass
