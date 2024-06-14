import aiosqlite
import disnake
from disnake.ext import commands

class UsersDataBase:
    def __init__(self):
        self.userdb = 'database/fileDB/users.db'
        self.logsdb = 'database/fileDB/logs.db'
        self.verifyMessagedb = 'database/fileDB/verifyMessage.db'
        
    async def create_table(self):
        async with aiosqlite.connect(self.userdb) as db:
            async with db.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                        userID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        userName TEXT NULL,
                                        age INTEGER NULL
                                    )''')
                await db.commit()
    
    async def create_table_log_chanel(self):
        async with aiosqlite.connect(self.logsdb) as db:
            async with db.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS logsChanel (
                                        guildID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        channelLogsID INTEGER NULL
                                    )''')
                await db.commit()
    
    async def insert_verify_user(self, interaction, member: disnake.Member):
        async with aiosqlite.connect(self.userdb) as db:
            async with db.cursor() as cursor:
                query = '''INSERT INTO users (userID, userName) VALUES (?, ?)'''
                await cursor.execute(query, (member.id, member.name))
                await db.commit()
            await interaction.send("Верефицирован", ephemeral=True)
            
    async def delete_verify_user(self, interaction, member: disnake.Member):
        async with aiosqlite.connect(self.userdb) as db:
            async with db.cursor() as cursor:
                query = '''DELETE FROM users WHERE userID = ?'''
                await cursor.execute(query, (member.id,))
                await db.commit()
            await interaction.send("Видалено", ephemeral=True)
            
    async def insert_logs_channel(self, interaction, channelLogs: disnake.TextChannel, guild_id):
        async with aiosqlite.connect(self.logsdb) as db:
            async with db.cursor() as cursor:
                query = '''INSERT INTO logsChanel (guildID, channelLogsID) VALUES (?, ?)'''
                await cursor.execute(query, (guild_id, channelLogs.id))
                await db.commit()
            await interaction.send("Добавлено", ephemeral=True)