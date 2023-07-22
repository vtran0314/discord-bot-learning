import discord
from .models import UserActivity, PointType
from users.models import User
from baseclasses.controller import Controller


class Ranks(Controller):
    
    
    async def process_message(self, message: discord.Message):
        await self.add_points(message.id, message.author.id, PointType.MESSAGE)
        #print(message.id)
        
        
    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        if payload.event_type == "REACTION_ADD":
            await self.add_points(payload.message_id, payload.user_id, PointType.REACTION)
        else:
            await self.reduce_points(payload.message_id, payload.user_id, PointType.REACTION, UserActivity.MODE_REDUCE)
        #print(payload.message_id)
    
    async def announcement(self, message):
        await self.messenger.send_message(message)
    
    async def _get_point_modifier(self, user_id):
        modifier = 1.0
        member = await self.bot_handler.fetch_member(user_id)
        special_role = await self.bot_handler.fetch_role("Gold Role")
        if special_role in member.roles:
            modifier = 2  
        return modifier
    
    #Private function that can only be used within the controller / Rank class
    async def _save_to_db(
        self,
        message_id: int,
        user_id: int,
        point_type: PointType,
        manual_points: int = 0, 
        mode: str = UserActivity.MODE_ADD    
    ):
        user = User.fetch_user_by_id(user_id)
        modifier = await self._get_point_modifier(user_id)
        user_activity = UserActivity(message_id=message_id, user=user)
        changed, number_levels, current_level = user_activity.record_new_points(point_type, mode, manual_points, modifier)
        
        
        if changed:
            member = await self.bot_handler.fetch_member(user_id)
            
            for i in range(number_levels):
                message = f"{member.display_name} has reach level `{current_level + i + 1}`"
                await self.announcement(message)    
    
    async def add_points(self, message_id, user_id, point_type, manual_points = 0):
        await self._save_to_db(message_id, user_id, point_type, manual_points = manual_points)
        
    async def reduce_points(self, message_id, user_id, point_type, mode: str):
        await self._save_to_db(message_id, user_id, point_type, mode = mode )
            