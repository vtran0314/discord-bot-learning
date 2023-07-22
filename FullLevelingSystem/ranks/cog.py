import discord
import settings
from discord.ext import commands
from users.models import User
from .models import LevelSystem, UserActivity, PointType
from .drawer import RankImage
from utils.checks import is_command_channel
from .checks import has_rank

class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    @is_command_channel()
    async def rs(self, ctx):
        ...
    
    @has_rank(5)
    async def shop(self,ctx):
        await ctx.send("This is our shop")
        
    @rs.command()
    async def leaderboard(self, ctx, limit: int = 10):
        if limit > 10:
            limit = 10
        leaderboard_users = User.get_leaderboard(limit)
        embed = discord.Embed(title="Leaderboard")
        output = "```"
        
        for user in leaderboard_users:
            discord_member = await ctx.message.guild.fetch_member(user.user_id)
            output += f"{discord_member.display_name:25} {user.total_points} Pts.\n"
        
        output += "```"
        
        embed.add_field(name="Users", value=output, inline = False)
        await ctx.send(embed=embed)
    
    @rs.command()
    async def rank(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
            
        total_points = UserActivity.get_points(member.id)       
        current_rank = LevelSystem.get_rank(total_points)    
        next_level_xp = LevelSystem.get_level_xp(current_rank+1)      
        current_xp_level = LevelSystem.get_level_xp(current_rank)    
        next_level_xp_diff  = next_level_xp - current_xp_level    
        level_progress = total_points - current_xp_level
        
        count_messages = UserActivity.count_message(member.id)
        count_reactions = UserActivity.count_reaction(member.id) 
        
        rank_image = RankImage()
        full_image_path = rank_image.draw_basic_information(
            member.display_name,
            total_points,
            current_rank,
            count_messages,
            count_reactions
        )
        
        rank_image.draw_progress_bar(
            full_image_path, next_level_xp_diff, level_progress
        )
        
        '''
        Changed discord.Member.avatar method
        
        Changed await member.avatar.save(member_avatar_path)
        To      avatar_asset = member.display_avatar
                await avatar_asset.save(str(member_avatar_path))
                
        Using member.avatar will raise NoneType error if user does not set global avatar
        which will return None value to discord.Member. 
        
        Thus, using member.display_avatar will return a default avatar of users if they don't have global avatar set. 
        
        '''
        avatar_asset = member.display_avatar
        
        member_avatar_path = settings.IMAGES_AVATAR_TMP_DIR / f"{member.id}.png"
        await avatar_asset.save(str(member_avatar_path))

        #await member.avatar.save(member_avatar_path)
        
        rank_image.draw_member_avatar(full_image_path, member_avatar_path)
        
        rank_card_image =  discord.File(full_image_path, "rank.png")
        
        embed = discord.Embed(title="My rank")
        embed.set_image(url = "attachment://rank.png")
        await ctx.send(embed=embed, file = rank_card_image)
        
        rank_image.delete_img(full_image_path)

    @rs.command()
    async def give(self, ctx, member: discord.Member, points: int):
        await self.bot.ranks.add_points(ctx.message.id, member.id, PointType.MANUAL, points)
    
async def setup(bot):
   await bot.add_cog(Ranks(bot))