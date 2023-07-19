from baseclasses.models import BaseModel
import peewee

class User(BaseModel):
    user_id = peewee.CharField(max_length=100)
    total_points = peewee.FloatField(default=0)
    
    @staticmethod
    def fetch_user_by_id(user_id):
        try:
            user = User.get(User.user_id==user_id)
        except:
            user = User.create(user_id=user_id)
        return user
    
    @staticmethod
    def get_leaderboard(limit: int = 10):
        return User.select().order_by(User.total_points.desc())[:limit]