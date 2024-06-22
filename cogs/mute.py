import datetime
import disnake
from disnake.ext import commands

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ограничеть пользователля")
    async def mute(self, interaction, member: disnake.Member, time: int, reason: str = None):
        time = datetime.datetime.now() + datetime.timedelta(minutes=time)
        await member.timeout(until=time, reason=reason)
        await interaction.response.send_message(
            f"Пользователь {member.mention} был затайм-аутен до {time.strftime('%H:%M:%S %d.%m.%Y')}",
            ephemeral=True
        )

    @commands.slash_command(description="Снять ограничения")
    async def unmute(self, interaction, member: disnake.Member):
        await member.timeout(until=None, reason=None)
        await interaction.response.send_message(
            f"Пользователь {member.mention} был разтайм-аутен",
            ephemeral=True
        )

def setup(bot):
    bot.add_cog(Timeout(bot))