import aiosqlite
import disnake

class WelcomeChannel:
    def __init__(self):
        self.botDatabase = "database/fileDB/BotDDatabase.db"
        
    async def create_table(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS welcomeChannel (
                                    guildId INTEGER PRIMARY KEY,
                                    channelId INTEGER
                                )''')
            await db.commit()
    
    async def get_welcome_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            cursor = await db.execute('SELECT channelId FROM welcomeChannel WHERE guildId = ?', (guild.id,))
            result = await cursor.fetchone()
            return result[0] if result else None
    
    async def add_welcome_channel(self, channel: disnake.TextChannel, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            await db.execute('''INSERT INTO welcomeChannel (guildId, channelId) VALUES (?, ?)
                                ON CONFLICT(guildId) DO UPDATE SET channelId=excluded.channelId''', (guild.id, channel.id))
            await db.commit()
                
    async def remove_channel(self, guild: disnake.Guild):
        async with aiosqlite.connect(self.botDatabase) as db:
            await db.execute('DELETE FROM welcomeChannel WHERE guildId = ?', (guild.id,))
            await db.commit()
