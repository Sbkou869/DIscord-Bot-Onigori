import aiosqlite
import disnake
from disnake.ext import commands

class WelcomeChannel:
    def __init__(self):
        self.botDatabase = "database/fileDB/BotDDatabase.db"
        
    async def create_table(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS welcomeChannel (
                                        guildId INTEGER PRIMARY KEY AUTOINCREMENT,
                                        channelId INTEGER NULL
                                    )''')
                await db.commit()
    
    async def get_welcome_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('SELECT channelId FROM welcomeChannel WHERE guildId = ?', (guild.id,))
                result = await cursor.fetchone()
                return guild.get_channel(result[0]) if result else None
    
    async def add_welcome_channel(self, channel: disnake.TextChannel, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('INSERT INTO welcomeChannel VALUES (?,?)', (guild.id, channel.id))
                await db.commit()
                
    async def remove_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM welcomeChannel WHERE guildId = ?', (guild.id,))
                await db.commit()
                