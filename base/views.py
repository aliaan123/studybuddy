from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
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
    form = RoomForm()
    if request.method == 'POST':
        # Passes in the request POST data into the form. 
        form = RoomForm(request.POST)
        # If the form has valid data, we save it and return to home. 
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)