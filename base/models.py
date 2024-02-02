from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# creating models of tables in the Rooms


# Topic class, represents the topic of the discussion.
# Rooms are children of the topic class
class Topic(models.Model):
    name = models.CharField(max_length = 200) # Name of the topic
    
    def __str__(self): # string representation of the topic
        return self.name

# Room class, represents a chat room.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True) # The actual user that is connected. Relationship to a host. 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True) # A topic can have multiple rooms, but a room can only have one topic. 
    name = models.CharField(max_length = 200) # Name of the room. 
    description = models.TextField(null = True, blank = True) # Description of room. Makes sure the values can be left blank. 
    #participants =  # Stores all the users active in a room
    updated = models.DateTimeField(auto_now = True) # Takes a snapshot of anytime the table (model instance) is updated. Takes a timestamp every time room is updated.
    created = models.DateTimeField(auto_now_add = True) # Takes a timestamp of when the instance was created.
    
    def __str__(self): # string representation of the room
        return self.name
    

# Message class, represents a message sent by a user in a room. 
# Has Room relationship and User relationship. Both are one to many relationships in the database. 
# Each room is going to have multiple messages, messages has only one room.
# Each user can have multiple messages, messages can only have one user. 
class Message(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User that is sending the message. Import user model from the django library. 
    
    # Foreign key used to establish the relationship in the database, and connect to the parent (Room).
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # When the parent (room) is deleted, the children (messages) are also deleted.
    body = models.TextField() # the actual message
    updated = models.DateTimeField(auto_now = True) # Takes a snapshot of anytime the table (model instance) is updated. Takes a timestamp every time room is updated.
    created = models.DateTimeField(auto_now_add = True) # Takes a timestamp of when the instance was created.
    
    def __str__(self): # string representation of the message
        return self.body[0:50] # trim it down, only the first 50 characters in the preview. 
    
      
    