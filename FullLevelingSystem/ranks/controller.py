import discord
from .models import UserActivity, PointType
from users.models import User


class Ranks:
    async def process_message(self, message: discord.Message):
        await self.add_points(message.id, message.author.id, PointType.MESSAGE)
        #print(message.id)
        
        
    async def process_reaction(self, payload: discord.RawReactionActionEvent):
        if payload.event_type == "REACTION_ADD":
            await self.add_points(payload.message_id, payload.user_id, PointType.REACTION)
        else:
            await self.reduce_points(payload.message_id, payload.user_id, PointType.REACTION, UserActivity.MODE_REDUCE)
        #print(payload.message_id)
    
    #Private function that can only be used within the controller / Rank class
    def _save_to_db(self, message_id: int, user_id: int, point_type: PointType, mode: str = UserActivity.MODE_ADD):
        user = User.fetch_user_by_id(user_id)
        user_activity = UserActivity(message_id=message_id, user=user)
        user_activity.record_new_points(point_type, mode)
    
    async def add_points(self, message_id, user_id, point_type):
        self._save_to_db(message_id, user_id, point_type)
        
    async def reduce_points(self, message_id, user_id, point_type, mode: str):
        self._save_to_db(message_id, user_id, point_type, mode)
        