import peewee
import datetime
import database

class BaseModel(peewee.Model):
    created = peewee.DateTimeField(default=datetime.datetime.now)
    modified = peewee.DateTimeField()
    
    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    
    class Meta:
        database = database.db