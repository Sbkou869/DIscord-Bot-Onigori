import disnake
import datetime
from disnake.ext import commands
from .game_buttons import GameButtons  # Використання відносного імпорту
from database.RankDatabase import RankDatabase

GLOBAL_DB = RankDatabase()

TIME = datetime.datetime.now()


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="game", description="Игры")
    async def game(self, interaction):
        view = GameButtons(interaction.author, GLOBAL_DB)
        embed = disnake.Embed(
            title="Игры",
            description="**В данном разделе вы можете выбрать во что сыграть:**\n\n",
            timestamp=TIME,
            color=disnake.Color.red()
        )
        
        embed.set_thumbnail(url=interaction.user.avatar.url)
        
        await interaction.response.send_message(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Game(bot))
