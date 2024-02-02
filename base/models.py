from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# creating models of tables in the Rooms

class Room(models.Model):
    #host = # The actual user that is connected
    #topic =
    name = models.CharField(max_length = 200) # Name of the room. 
    description = models.TextField(null = True, blank = True) # Description of room. Makes sure the values can be left blank. 
    #participants =  # Stores all the users active in a room
    updated = models.DateTimeField(auto_now = True) # Takes a snapshot of anytime the table (model instance) is updated. Takes a timestamp every time room is updated.
    created = models.DateTimeField(auto_now_add = True) # Takes a timestamp of when the instance was created.
    
    def __str__(self): # string representation of the room
        return self.name
    
# Message class. Each room is going to have multiple messages. One to many relationship in the database.  
class Message(models.Model):
    #user =  # user that is sending the message
    # Foreign key used to establish the relationship in the database, and connect to the parent (Room).
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # When the parent (room) is deleted, the children (messages) are also deleted.
    body = models.TextField() # the actual message
    updated = models.DateTimeField(auto_now = True) # Takes a snapshot of anytime the table (model instance) is updated. Takes a timestamp every time room is updated.
    created = models.DateTimeField(auto_now_add = True) # Takes a timestamp of when the instance was created.
    
    def __str__(self): # string representation of the message
        return self.body[0:50] # trim it down, only the first 50 characters in the preview. 
    
      
    