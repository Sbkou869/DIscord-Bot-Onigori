import aiosqlite
import disnake

class UsersDataBase:
    def __init__(self):
        self.name = 'dbs/users.db'

    async def setup(self):
        async with aiosqlite.connect(self.name) as db:
            await self.create_table()

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            query = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                money INTEGER,
                premium INTEGER
            )'''
            await db.execute(query)
            await db.commit()

    async def get_user(self, member):
        async with aiosqlite.connect(self.name) as db:
            query = 'SELECT * FROM users WHERE id=?'
            cursor = await db.execute(query, (member.id,))
            user_data = await cursor.fetchone()

            if not user_data:
                return (member.id, 0, 0)

            return (user_data[0], user_data[1], user_data[2])

    async def add_user(self, user: disnake.Member):
        if not await self.get_user(user):
            async with aiosqlite.connect(self.name) as db:
                query = 'INSERT INTO users (id, money, premium) VALUES (?, ?, ?)'
                await db.execute(query, (user.id, 0, 0))
                await db.commit()

    async def update_money(self, user: disnake.Member, money: int, premium: int):
        async with aiosqlite.connect(self.name) as db:
            query = 'SELECT money, premium FROM users WHERE id = ?'
            cursor = await db.execute(query, (user.id,))
            current_data = await cursor.fetchone()

            if not current_data:
                return False

            current_money, current_premium = current_data

            if current_money + money < 0 or current_premium + premium < 0:
                return False  # Если пользователь не имеет достаточно денег для "забирания"

            query = 'UPDATE users SET money = money + ?, premium = premium + ? WHERE id = ?'
            await db.execute(query, (money, premium, user.id))
            await db.commit()

            return True  # Успешное выполнение обновления базы данных

    async def get_top(self):
        async with aiosqlite.connect(self.name) as db:
            query = 'SELECT * FROM users ORDER BY money DESC'
            cursor = await db.execute(query)
            return await cursor.fetchall()
