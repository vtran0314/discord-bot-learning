import settings
from discord.ext import commands
from .models import UserActivity, LevelSystem

def has_rank(rank: int):
    def predicate(ctx):
        current_points = UserActivity.get_points(ctx.message.author.id)
        current_level = LevelSystem.get_rank(current_points)
        if current_level > rank:
            return True
        return False
        
    return commands.check(predicate)
        