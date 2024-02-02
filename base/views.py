# Import necessary modules from Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# rooms = [
#    {"id":1, "name":"Lets learn python!"},
#    {"id":2, "name":"Design with me!"},
#    {"id":3, "name":"Frontend developers!"},
# ]

# Define views for the application

# This function retrieves all rooms from the database 
# and passes them to the "base/home.html" template using the Django render function. 
# This template is responsible for displaying the list of rooms.
def home(request): 
    # Query all rooms from the Room model (database table) and pass them to the template
    rooms = Room.objects.all() 
    context = {"rooms" : rooms}
    return render(request, "base/home.html", context)

#  Fetches a specific room based on the provided primary key (pk) from the URL. 
# The room is then passed to the "base/room.html" template.
def room(request, pk):
    # Retrieve a single room from the database based on the provided id (pk)
    room = Room.objects.get(id=pk) 
    context = {"room" : room}
    return render(request, "base/room.html", context)


# Handles the creation of a new room. It initializes a RoomForm, processes the form data on a POST request, 
# saves the room to the database if valid, and redirects to the home page.
def createRoom(request):
    # Initialize a RoomForm instance
    form = RoomForm()
    if request.method == 'POST':
        # If the request method is POST, populate the form with the provided POST data
        form = RoomForm(request.POST)
        # If the form is valid, save the data to the database and redirect to the home page
        if form.is_valid():
            form.save()
            return redirect('home')
    # Prepare the form to be rendered in the template
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

# Allows us to update a specific room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # the form will be prefilled with the room value.
    
    ## Check if it is a POST method
    if request.method == 'POST':
        # The data in the POST method is going to replace whatever value is changed in the room with the new value written in the room form. 
        form = RoomForm(request.POST, instance=room)
        # If the form is valid, save the data to the database and redirect to the home page
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)
    