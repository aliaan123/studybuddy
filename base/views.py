from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.

# rooms = [
#    {"id":1, "name":"Lets learn python!"},
#    {"id":2, "name":"Design with me!"},
#    {"id":3, "name":"Frontend developers!"},
# ]

def home(request): 
    rooms = Room.objects.all() # query for rooms. Gives us all the rooms in the database. This is passed into the template.
    context = {"rooms" : rooms}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk) # gets a single room from the database based on the unique id. 
    context = {"room" : room}
    return render(request, "base/room.html", context)


def createRoom(request):
    context = {}
    return render(request, 'base/room_form.html', context)