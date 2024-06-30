import shutil
import schedule
import asyncio
import os
import pytz
from datetime import datetime
from disnake.ext import commands, tasks

database_file = "database/fileDB/BotDDatabase.db"
backup_location = "database/backup/BotDDatabase_backup.db"
time_zone = pytz.timezone("Europe/Kiev")

class BackupDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedule_backup_task()

    async def backup_database(self):
        try:
            if os.path.exists(backup_location):
                os.remove(backup_location)
            shutil.copy(database_file, backup_location)
            print(f"Резервная копия {database_file} успешно создана в {backup_location}")
        except Exception as e:
            print(f"Ошибка при создании резервной копии: {e}")

    def scheduled_backup(self):
        asyncio.create_task(self.backup_database())

    def schedule_backup_task(self):
        # Планирование задачи на каждое воскресенье в 16:50 по Киеву
        schedule.every().sunday.at("16:55").do(self.scheduled_backup)

        @tasks.loop(seconds=60)
        async def run_scheduler():
            schedule.run_pending()
            print(f"Current Kyiv Time: {datetime.now(time_zone).strftime('%H:%M')}")

        run_scheduler.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded")

def setup(bot):
    bot.add_cog(BackupDB(bot))
