import disnake
from disnake.ext import commands
import os
import sys
from dotenv import load_dotenv
from database.UserInfoDatabase import UsersDataBase

load_dotenv("config/config.env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

global_db = UsersDataBase()
intents = disnake.Intents.all()
intents.message_content = True
prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

@bot.event
async def on_member_remove(member: disnake.Member):
    await global_db.delete_user_from_all_databases(member.id)


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
    
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

token = os.getenv ('TEST')
bot.run(token)
