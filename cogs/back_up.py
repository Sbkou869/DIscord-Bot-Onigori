import disnake
from disnake.ext import commands, tasks
import aiosqlite
import shutil
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from colorama import init, Fore, Style

import asyncio

init()


class BackupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ''  # ID Владельца
        self.gmail_user = ''
        self.gmail_password = '' # Пароль приложений

        # Настройка задачи резервного копирования
        self.backup_task.start()

        # Время последнего резервного копирования
        self.last_backup_time = datetime.now()

        # Запуск задачи обновления таймера
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.update_timer())

    @tasks.loop(seconds=259200)  # 259200 секунд = 3 дня
    async def backup_task(self):
        await self.perform_backup()

    async def perform_backup(self):
        db_path = 'database/fileDB/BotDDatabase.db'
        backup_path = 'database/backUP/BDatabase.db'
        receiver_email = '' # Почта на которую отправлять
        subject = 'Еженедельный бекап БД'
        body = 'Ваш бекап БД за неделю.'

        await self.backup_database(db_path, backup_path)
        self.send_email(receiver_email, subject, body, backup_path)
        
        # Обновляем время последнего резервного копирования
        self.last_backup_time = datetime.now()
        print(f"{Fore.GREEN}Backup completed at {Fore.RED}{self.last_backup_time.strftime('%Y-%m-%d %H:%M:%S')}")

    async def backup_database(self, db_path: str, backup_path: str):
        if not os.path.exists(os.path.dirname(backup_path)):
            os.makedirs(os.path.dirname(backup_path))

        async with aiosqlite.connect(db_path) as db:
            await db.execute('VACUUM')
            await db.commit()
        shutil.copyfile(db_path, backup_path)

    def send_email(self, receiver_email, subject, body, attachment_path):
        msg = MIMEMultipart()
        msg['From'] = self.gmail_user
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.gmail_user, receiver_email, msg.as_string())

    @commands.slash_command(name="backup", description="Создает внеплановый бекап базы данных и отправляет на почту")
    async def manual_backup(self, inter: disnake.ApplicationCommandInteraction):
        if str(inter.author.id) != self.owner_id:
            await inter.send("У вас нет прав на выполнение этой команды.", ephemeral=True)
            return

        await self.perform_backup()
        await inter.send("Внеплановый бекап базы данных создан и отправлен на почту.")

    async def update_timer(self):
        while True:
            next_backup_time = self.last_backup_time + timedelta(days=3)
            time_until_next_backup = next_backup_time - datetime.now()
            print(f"{Fore.GREEN}Time until next backup: {Fore.YELLOW}{str(time_until_next_backup).split('.')[0]}", end='\r')
            await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(BackupCog(bot))
