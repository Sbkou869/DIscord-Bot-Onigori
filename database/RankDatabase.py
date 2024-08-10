import aiosqlite
import random
import disnake
from disnake.ext import commands

rnd_score = random.randint(3, 16)

class RankDatabase:
    def __init__(self, bot):
        self.bot = bot
        self.botDatabase = "database/fileDB/BotDDatabase.db"
        
    async def create_table(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS economy (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        userName TEXT NULL,
                                        level INTEGER NULL,
                                        score INTEGER NULL,
                                        new_score INTEGER NULL,
                                        coins INTEGER NULL,
                                        rubins INTEGER NULL
                                    )''')
                await db.commit()

    async def get_user(self, user_id: int):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM economy WHERE id = ?'
                await cursor.execute(query, (user_id,))
                return await cursor.fetchone()

    async def get_coins(self, user: disnake.Member):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'SELECT coins FROM economy WHERE id = ?'
                await cursor.execute(query, (user.id,))
                coins = await cursor.fetchone()
                return coins[0] if coins else None

    async def get_rubyns(self, user: disnake.Member):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'SELECT rubins FROM economy WHERE id = ?'
                await cursor.execute(query, (user.id,))
                rubins = await cursor.fetchone()
                return rubins[0] if rubins else None

    async def add_user(self, member: disnake.Member):
        async with aiosqlite.connect(self.botDatabase) as db:
            if not await self.get_user(member.id):
                async with db.cursor() as cursor:
                    query = 'INSERT INTO economy (id, userName, level, score, new_score, coins, rubins) VALUES (?, ?, ?, ?, ?, ?, ?)'
                    await cursor.execute(query, (member.id, member.name, 1, 100, 0, 0, 0))
                    await db.commit()
                    
    async def update_money(self, user: disnake.Member, coins: int):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE economy SET coins = coins + ? WHERE id = ?'
                await cursor.execute(query, (coins, user.id))
                await db.commit()

    async def update_ruby(self, user: disnake.Member, rubins: int):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE economy SET rubins = rubins + ? WHERE id = ?'
                await cursor.execute(query, (rubins, user.id))
                await db.commit()
                
    async def update_score(self, user_id):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = f'UPDATE economy SET score = score + ? WHERE id = ?'
                await cursor.execute(query, (rnd_score, user_id))
                await db.commit()
                
    async def update_level(self, user_id):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT score, level FROM economy WHERE id = ?', (user_id,))
                result = await cursor.fetchone()
                if result:
                    score, level = result
                    new_level_score = 2 ** level * 100  # Рассчитываем необходимое количество очков для достижения нового уровня

                    if score >= new_level_score:
                        await cursor.execute('''
                            UPDATE economy
                            SET level = level + 1, rubins = rubins + 15, coins = coins + 500, new_score = ?
                            WHERE id = ?
                        ''', (new_level_score * 2, user_id))
                        await db.commit()
                        
                        user = await self.bot.fetch_user(user_id)
                        await user.send(f"Ваш уровень повысился. Ваша награда: 15 рубинов и 500 монет.")
                        # print(f"Не удалось найти текстовый канал 'название_текстового_канала'")
                    else:
                        pass
                        # print("У пользователя недостаточно очков для повышения уровня.")
                else:
                    pass
                    # print("Пользователь не найден в базе данных экономики.")


    async def stavka_dekrement(self, user_id, count):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = f'UPDATE economy SET coins = coins - ? WHERE id = ?'
                await cursor.execute(query, (count, user_id))
                await db.commit()

    async def stavka_increment(self, user_id, count):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = f'UPDATE economy SET coins = coins + ? WHERE id = ?'
                await cursor.execute(query, (count, user_id))
                await db.commit()

    async def stavka_vabank(self, user_id, count):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = f'UPDATE economy SET coins = coins + ? WHERE id = ?'
                await cursor.execute(query, (count, user_id))
                await db.commit()

    async def buy_coins(self, user_id, sum_coins, rubins):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = f'UPDATE economy SET coins = coins + ?, rubins = rubins - ? WHERE id = ?'
                await cursor.execute(query, (sum_coins, rubins, user_id))
                await db.commit()

    async def get_top_money(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM economy ORDER BY coins DESC'
                await cursor.execute(query)
                return await cursor.fetchall()

    async def get_top_ruby(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM economy ORDER BY rubins DESC'
                await cursor.execute(query)
                return await cursor.fetchall()

    async def get_top_score(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM economy ORDER BY score DESC'
                await cursor.execute(query)
                return await cursor.fetchall()
