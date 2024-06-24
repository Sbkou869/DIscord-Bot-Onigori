import disnake
from disnake import File
from disnake.ext import commands
from easy_pil import Editor, load_image_async, Font
from database.Welcome_Channel import WelcomeChannel



class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        await self.generate_welcome_image(member)
        
    @commands.command(name="test_welcome")
    async def test_welcome(self, ctx, member: disnake.Member = None):
        """Тестовая команда для проверки приветственного сообщения."""
        if member is None:
            member = ctx.author  # Используем автора команды, если член не указан
        await self.generate_welcome_image(member, test_channel=ctx.channel)
   
   
    async def generate_welcome_image(self, member: disnake.Member, test_channel=None):
        guild = member.guild
        welcome_db = WelcomeChannel()
        channel = await welcome_db.get_welcome_channel(guild) if not test_channel else test_channel
        
        background = Editor("image\welcome_baner\pic.jpg")
        profile_image = await load_image_async(str(member.avatar.url))
        
        profile = Editor(profile_image).resize((250, 250)).circle_image()
        popins = Font.poppins(size=70, variant="bold")
        popins_small = Font.poppins(size=50, variant="bold")
        
        background.paste(profile, (525, 175))
        background.ellipse((525, 175), 250, 250, outline="white", stroke_width=5)
        
        background.text((650, 450), f"WELCOME  {member.name}", color=0x6f7575, font=popins, align="center")
        background.text((600, 520), f"{member.guild.name}", color=0x6f7575, font=popins_small, align="center")
        
        file = File(fp=background.image_bytes, filename="pic.jpg")
        await channel.send(file=file)
        
        
def setup(bot):
    bot.add_cog(Welcome(bot))      