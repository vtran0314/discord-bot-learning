import settings
from discord.ext import commands

class BotHandler:
    
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetch_guild(self):
        return await self.bot.fetch_guild(settings.GUILD_ID)


    async def fetch_member(self, user_id):
        guild = await self.fetch_guild()
        return await guild.fetch_member(user_id)
    
    async def fetch_role(self, role_name: str):
        guild = await self.fetch_guild()
        roles = await guild.fetch_roles()
        for role in roles:
            if role.name == role_name:
                return role
        return None
