import disnake
import datetime
import random
from disnake.ext import commands
from database.RankDatabase import RankDatabase


TIME = datetime.datetime.now


class CostiModalMoney(disnake.ui.Modal):
    def __init__(self, member: disnake.Member, bot):
        self.member = member
        self.bot = bot
        self.global_db = RankDatabase(bot)
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
            curentMoney = await self.global_db.get_coins(self.member)

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
                    await self.global_db.stavka_increment(self.member.id, stavka )
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
                    await self.global_db.stavka_dekrement(self.member.id, stavka)
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
    def __init__(self, member: disnake.Member, bot):
        super().__init__(timeout=None)
        self.member = member
        self.bot = bot
        self.global_db = RankDatabase(bot)

    @disnake.ui.button(label="Сделать ставку за монеты", style=disnake.ButtonStyle.blurple)
    async def btMoneyStavka(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            if not self.member:
                await interaction.response.defer()
            else:
                await interaction.response.send_modal(CostiModalMoney(self.member, self.bot))
        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")

    @disnake.ui.button(label="Ва-банк", style=disnake.ButtonStyle.blurple)
    async def btVabank(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            if not self.member:
                await interaction.response.defer()
            else:
                
                curentMoney = await self.global_db.get_coins(self.member)
                
                if curentMoney == 0:
                    await interaction.response.send_message("У вас недостаточно монет для ставки.")
                else:
                    curent_money = await self.global_db.get_coins(self.member)
                    num_user_first = int(random.choice('123456'))
                    num_user_last = int(random.choice('123456'))
                    user_sum = num_user_first + num_user_last

                    num_bot_first = int(random.choice('123456'))
                    num_bot_last = int(random.choice('123456'))
                    bot_sum = num_bot_first + num_bot_last

                    if user_sum > bot_sum:
                        await self.global_db.stavka_vabank(self.member.id, curent_money)
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
                        await self.global_db.stavka_dekrement(self.member.id, curent_money)
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

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.gray)
    async def btBack(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        try:
            view = GameButtons(self.member, self.bot)
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


class SelectShop(disnake.ui.Select):
    def __init__(self, member:disnake.Member, bot):
        self.member = member
        self.bot = bot
        self.global_db = RankDatabase(bot)
        options = [
            disnake.SelectOption(
                label="1. Пак базовый ",
                value="base",
                emoji="<:GlowingStar:1251937859263402145>"
            ),
            disnake.SelectOption(
                label="2. Пак продвинутый",
                value="adept",
                emoji="<:GlowingStar:1251937859263402145>"
            ),
            disnake.SelectOption(
                label="3. Пак богач",
                value="main",
                emoji="<:GlowingStar:1251937859263402145>"
            ),
            disnake.SelectOption(
                label="4. Пак ультра ",
                value="ultra",
                emoji="<:GlowingStar:1251937859263402145>"
            ),
            disnake.SelectOption(
                label="5. Пак милионера",
                value="milioner",
                emoji="<:GlowingStar:1251937859263402145>"
            ),
        ]
        super().__init__(placeholder="Выберите пак", options=options, custom_id="magazin", min_values=1, max_values = 1)

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

        chosen_value = interaction.values[0]

        if chosen_value == "base":
            price = 20
            curent_ruby = await self.global_db.get_rubyns(self.member)
            if curent_ruby < price:
                await interaction.followup.send("У вас недостаточно рубинов.", ephemeral = True)
            else:
                await self.global_db.buy_coins(self.member.id, 60000+10000, price)
                await interaction.followup.send(f"{self.member.mention} успешно начислено. Проверте баланс: `/mycard`",
                                                ephemeral=True)

        elif chosen_value == "adept":
            price = 80
            curent_ruby = await self.global_db.get_rubyns(self.member)
            if curent_ruby < price:
                await interaction.followup.send("У вас недостаточно рубинов.", ephemeral = True)
            else:
                await self.global_db.buy_coins(self.member.id, 100000 + 25000, price)
                await interaction.followup.send(f"{self.member.mention} успешно начислено. Проверте баланс: `/mycard`",
                                                ephemeral=True)

        elif chosen_value == "main":
            price = 170
            curent_ruby = await self.global_db.get_rubyns(self.member)
            if curent_ruby < price:
                await interaction.response.send_message("У вас недостаточно рубинов.", ephemeral = True)
            else:
                await self.global_db.buy_coins(self.member.id, 250000 + 50000, price)
                await interaction.followup.send(f"{self.member.mention} успешно начислено. Проверте баланс: `/mycard`",
                                                ephemeral=True)

        elif chosen_value == "ultra":
            price = 300
            curent_ruby = await self.global_db.get_rubyns(self.member)
            if curent_ruby < price:
                await interaction.followup.send("У вас недостаточно рубинов.", ephemeral = True)
            else:
                await self.global_db.buy_coins(self.member.id, 500000 + 200000, price)
                await interaction.followup.send(f"{self.member.mention} успешно начислено. Проверте баланс: `/mycard`",
                                                ephemeral=True)
        elif chosen_value == "milioner":
            price = 550
            curent_ruby = await self.global_db.get_rubyns(self.member)
            if curent_ruby < price:
                await interaction.followup.send("У вас недостаточно рубинов.", ephemeral = True)
            else:
                await self.global_db.buy_coins(self.member.id, 700000 + 500000, price)
                await interaction.followup.send(f"{self.member.mention} успешно начислено. Проверте баланс: `/mycard`",
                                                ephemeral=True)

        print(f"Пользователь {interaction.author} выбрал: {chosen_value}")

class GameButtons(disnake.ui.View):
    def __init__(self, member: disnake.Member, bot):
        super().__init__(timeout=None)
        self.member = member
        self.bot = bot
        self.global_db = RankDatabase(bot)

    @disnake.ui.button(label="Кости", style=disnake.ButtonStyle.green)
    async def btroulette(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            member = self.member
            user = await self.global_db.get_user(member.id)

            view = CostiButtons(member, self.bot)

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

    @disnake.ui.button(label="Магазин", style=disnake.ButtonStyle.blurple)
    async def btMagazin(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        try:
            member = self.member
            view = disnake.ui.View(timeout=None)
            user = await self.global_db.get_user(member.id)


            view = view.add_item(SelectShop(member, self.bot))

            embed = disnake.Embed(
                title="Магазин",
                description=(
                    f"**Вы можете купить монеты за рубины:.**\n\n"
                    f"**`1` - <:Ruby:1251937860672684163> `20`  => <:Coin:1251937857782808586> `60.000 + 10.000` **\n"
                    f"**`2` - <:Ruby:1251937860672684163> `80`  => <:Coin:1251937857782808586> `100.000 + 25.000` **\n"
                    f"**`3` - <:Ruby:1251937860672684163> `170` => <:Coin:1251937857782808586> `250.000 + 50.000` **\n"
                    f"**`4` - <:Ruby:1251937860672684163> `300` => <:Coin:1251937857782808586> `500.000 + 200.000` **\n"
                    f"**`5` - <:Ruby:1251937860672684163> `550` => <:Coin:1251937857782808586> `700.000 + 500.000` **\n"
                ),
                color=disnake.Color.red(),
            )

            embed.add_field(name='<:Coin:1251937857782808586> Деньги', value=f'```{user[5]}```')
            embed.add_field(name='<:Ruby:1251937860672684163> Рубины', value=f'```{user[6]}```')
            embed.set_image(file=disnake.File("image/icons/Magazin_Coin.png"))

            await interaction.response.edit_message(embed=embed, view=view)

        except Exception as e:
            await interaction.response.send_message(f"Ошибка: {e}")


def setup (bot):
    pass
