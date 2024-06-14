import disnake
from disnake.ext import commands
import os
import sys
from dotenv import load_dotenv

load_dotenv("config/config.env")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    activity=disnake.Streaming(
      name="Resting",
      url="https://www.youtube.com/watch?v=jfKfPfyJRdk&ab_channel=LofiGirl"))
    
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

token = os.getenv ('TOKEN')
bot.run(token)
