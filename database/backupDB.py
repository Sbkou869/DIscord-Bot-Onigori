import shutil
import schedule
import asyncio
import os

database_file = "database/fileDB/BotDDatabase.db"
backup_location = "database/backup/BotDDatabase_backup.db"


async def backup_database():
    try:
        if os.path.exists(backup_location):
            os.remove(backup_location)
        shutil.copy(database_file, backup_location)
        print(f"Резервная копия {database_file} успешно создана в {backup_location}")
    except Exception as e:
        print(f"Ошибка при создании резервной копии: {e}")


async def scheduled_backup():
    schedule.every().saturday.at("03:00").do(backup_database)

    while True:
        await asyncio.sleep(60)
        schedule.run_pending()
        print("Cheack time")
