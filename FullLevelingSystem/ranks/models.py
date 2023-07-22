import enum
import math
import peewee
from users.models import User
from baseclasses.models import BaseModel

class PointType(enum.Enum):
    MESSAGE = 2
    REACTION = 1
    MANUAL = 0
    
class LevelSystem():
    @staticmethod
    def get_rank(points: float | int):
        return math.floor((points * 5 / 4)** (1.0 / 3))
    
    @staticmethod
    def get_level_xp(level: int):
        return math.floor((4 * (level**3)) / 5)
    
    @staticmethod
    def level_changed(current_points, new_points):
        changed = False
        current_level = LevelSystem.get_rank(current_points)
        new_level = LevelSystem.get_rank(new_points)
        
        #Set change
        if current_level != new_level:
            changed = True
        number_levels = new_level - current_level
        
        return changed, number_levels, current_level
    
class UserActivity(BaseModel):
    
    MODE_ADD = "ADD"
    MODE_REDUCE = "REDUCE"
    MODE_CHOICES = (
        (MODE_ADD, MODE_ADD),
        (MODE_REDUCE, MODE_REDUCE),
    )
    
    user = peewee.ForeignKeyField(model=User)
    message_id = peewee.CharField(max_length=255)
    reaction = peewee.BooleanField(default=False)
    points = peewee.FloatField()
    mode = peewee.CharField(choices=MODE_CHOICES, default=MODE_ADD)
    
    def record_new_points(self, point_type: PointType, mode: str, manual_points = 0, modifier = 1.0):
        
        points = point_type.value
        
        
        if point_type == PointType.REACTION:
                self.reaction = True
        
        points = points * modifier
        
        if point_type == PointType.MANUAL:
                points = manual_points
        
        current_total_points =UserActivity.get_points(self.user.user_id)
        
        if mode == UserActivity.MODE_ADD:
            new_total_points = current_total_points + points
        else:
            new_total_points = current_total_points - points
        
        self.user.total_points = new_total_points
        self.user.save()
        
        self.points = points
        self.mode = mode
        self.save() #Inherent from UserActivity(BaseModel)
        
        return LevelSystem.level_changed(current_total_points, new_total_points)
        
    @staticmethod
    def get_points(user_id):
        added_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias("total")
        ).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_ADD)
        '''
            Output SQL syntax - print (added_points_sum)
            
            SQL FORM OF ADD
        SELECT "t1"."points", SUM("t1"."points") 
        AS "total" FROM "useractivity" AS "t1" 
        INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id") 
        WHERE (("t2"."user_id" = '<0123456789>') AND ("t1"."mode" = 'ADD'))
        '''
        
        reduced_points_sum = UserActivity.select(
            UserActivity.points, peewee.fn.SUM(UserActivity.points).alias("total")
        ).join(User).where(User.user_id == user_id, UserActivity.mode == UserActivity.MODE_REDUCE)
        '''
            Output SQL syntax - print (reduced_points_sum)
            SQL FORM OF REDUCE
        SELECT "t1"."points", SUM("t1"."points") 
        AS "total" FROM "useractivity" AS "t1" 
        INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id") 
        WHERE (("t2"."user_id" = '<0123456789>') AND ("t1"."mode" = 'REDUCE'))
        '''
        added_total = 0
        if added_points_sum[0].total: #<-- added .total to fix NoneType error 
            '''
            There was a non-type error here, so we fixed it by add .total to the end.
            Why?
            
            print(type(added_points_sum)) return with a <class 'peewee.ModelSelec'>
            print(type(added_points_sum[0])) return with Mode:UserActivity object
            
            Through this, I understand that only using the  added_points_sum[0] only return
            the object without its value, therefore, we need to add .total to return the object value

            '''
            added_total = added_points_sum[0].total 
        
        reduced_total = 0
        if reduced_points_sum[0].total:
            reduced_total = reduced_points_sum[0].total
        
        #not yet check for negative
        
        return added_total - reduced_total
    
    
    @staticmethod
    def count_message(user_id):
        return (
            UserActivity.select(UserActivity, User)
            .join(User)
            .where(User.user_id == user_id, UserActivity.reaction == False)
            .count())
    
    @staticmethod
    def count_reaction(user_id):
        
        added_reactions = (
            UserActivity.select(UserActivity, User)
            .join(User)
            .where(User.user_id == user_id, UserActivity.reaction == True, UserActivity.mode == UserActivity.MODE_ADD)
            .count()
            )
        
        reduced_reactions = (
            UserActivity.select(UserActivity, User)
            .join(User)
            .where(User.user_id == user_id, UserActivity.reaction == True, UserActivity.mode == UserActivity.MODE_REDUCE)
            .count()
            )
        
        return added_reactions - reduced_reactions
    
    
    