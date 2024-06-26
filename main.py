import disnake
from disnake.ext import commands
import os
import sys
from dotenv import load_dotenv
from database.backupDB import scheduled_backup

from database.UserInfoDatabase import UsersDataBase
from database.AdminsListDB import AdminListDatabase
from database.AutoroleDB import AutoRoleDanabase
from database.LogsDatabase import LogsDatabase
from database.Welcome_Channel import WelcomeChannel


load_dotenv("config/config.env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

global_db = UsersDataBase()
intents = disnake.Intents.all()
intents.message_content = True
prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")
  await bot.change_presence(
    status=disnake.Status.online,
    activity=disnake.Activity(
        type=disnake.ActivityType.streaming,
        name="Watching YouTube",
        url="https://www.youtube.com/watch?v=y3Q2fRqLlFk"
    ))
  await scheduled_backup()
  
  logs_db = LogsDatabase()
  users_db = UsersDataBase()
  welcome_channel_db = WelcomeChannel()
  autorole_db = AutoRoleDanabase()
  admin_list_db = AdminListDatabase()
    
  await logs_db.create_table_log_chanel()
  await users_db.create_table()
  await users_db.create_table_warns()
  await logs_db.create_table_log_chanel()
  await welcome_channel_db.create_table()
  await autorole_db.create_table_autorole()
  await admin_list_db.create_table_admins_list()


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

token = os.getenv ('STABLE')
bot.run(token)
