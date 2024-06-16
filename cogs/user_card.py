import disnake

from disnake.ext import commands
from database.RankDatabase import RankDatabase

global_db = RankDatabase()

class UserPanell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="mycard", description="Карточка пользователя")
    @commands.is_owner()
    async def mycard(self, interaction, member: disnake.Member = None):
        await global_db.create_table()  
        if not member:
            member = interaction.author
        await global_db.add_user(member)
        user = await global_db.get_user(member)  
        
        
        embed = disnake.Embed(color=0xf24e4e, title=f'Карточка пользователя - {user[1]}')
        embed.add_field(name='<:Coin:1251937857782808586> Деньги', value=f'```{user[5]}```') 
        embed.add_field(name='<:Ruby:1251937860672684163> Премиум', value=f'```{user[6]}```')  
        embed.add_field(name='<:ChevronUp:1251937855912280115> Уровень', value=f'```{user[2]}```')  
        embed.add_field(name='<:GlowingStar:1251937859263402145> Опыт', value=f'```{user[3]} / {user[4]}```')  
        embed.set_thumbnail(url=member.display_avatar.url)  
        await interaction.response.send_message(embed=embed)  
    
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.bot.user:
            return
        elif len(message.content) == 1:
            return
        else:
            await global_db.update_level(message.author.id)   
            await global_db.update_score(message.author.id)
    
def setup(bot):
    bot.add_cog(UserPanell(bot))