from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

# Registers the Room, Topic, and Message models with the Django admin interface,
# allowing administrators to manage these models through the admin site.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)

