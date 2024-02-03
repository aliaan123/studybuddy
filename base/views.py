# Import necessary modules from Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#    {"id":1, "name":"Lets learn python!"},
#    {"id":2, "name":"Design with me!"},
#    {"id":3, "name":"Frontend developers!"},
# ]

# Define views for the application


# Function for logging in a user
def loginPage(request):
    
    # Checks if a POST request was sent. 
    if request.method == 'POST':
        # Get the username and password from the data sent in the POST request. 
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Checks if the user exists with a try catch block. 
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        # Gets user object based on username and password.
        # Authenticate method will either give us an error or return back a user that matches the credentials (username and password).
        user = authenticate(request, username=username, password=password)
        
        # Logs the user in if there is one, and returns home. 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
                
    
    context = {}
    return render(request, 'base/login_register.html', context)    

# Function for logging out a user. 
def logoutUser(request):
    logout(request)
    return redirect('home')


# This function retrieves rooms from the database 
# and passes them to the "base/home.html" template using the Django render function. 
# This template is responsible for displaying the list of rooms.
def home(request): 
    # Query rooms from the Room model (database table) and pass them to the template

   # Retrieves the value of the 'q' parameter from the request's GET parameters. If 'q' is not present, it defaults to an empty string.    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # Queries the Room model (database table) to filter rooms based on the topic name containing the query (q). The __icontains lookup is used for a case-insensitive search.
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )  # we can now search by three different values: topic_name, name and description.
    # __ is used for quering upwards to the parent. 
    # Retrieves all topics from the Topic model.
    topics = Topic.objects.all()
    # Counts the number of rooms
    room_count = rooms.count()
    
    # Creates a dictionary context containing the queried rooms and all topics. This data will be passed to the template for rendering.
    context = {"rooms" : rooms, 'topics': topics, 'room_count' : room_count}
    # Uses the render function to render the "base/home.html" template with the provided context.
    return render(request, "base/home.html", context)

#  Fetches a specific room based on the provided primary key (pk) from the URL. 
# The room is then passed to the "base/room.html" template.
def room(request, pk):
    # Retrieve a single room from the database based on the provided id (pk)
    room = Room.objects.get(id=pk) 
    # Creates a dictionary context containing the retrieved room. This data will be passed to the template for rendering.
    context = {"room" : room}
    # Uses the render function to render the "base/room.html" template with the provided context.
    return render(request, "base/room.html", context)


# Handles the creation of a new room. It initializes a RoomForm, processes the form data on a POST request, 
# saves the room to the database if valid, and redirects to the home page.
def createRoom(request):
    # Initializes a new instance of the RoomForm class.
    form = RoomForm()
    # Checks if the request method is POST.
    if request.method == 'POST':
        # If the request method is POST, populate the form with the provided POST data
        form = RoomForm(request.POST)
        # If the form is valid, save the data to the database and redirect to the home page
        if form.is_valid():
            form.save()
            return redirect('home')
    # Creates a dictionary context containing the form. This data will be passed to the template for rendering.
    context = {'form':form}
    # Uses the render function to render the "base/room_form.html" template with the provided context.
    return render(request, 'base/room_form.html', context)

# Defines a function named updateRoom that takes a request object and a pk (primary key) parameter.
# Allows us to update a specific room
def updateRoom(request, pk):
    # Retrieves a specific room based on the provided pk.
    room = Room.objects.get(id=pk)
    # Initializes a form instance with the existing room data (instance=room). 
    form = RoomForm(instance=room) # the form will be prefilled with the room value.
    
    # Check if it is a POST method
    if request.method == 'POST':
        # Populates the form with the provided POST data, replacing the values in the form with the new values.
        form = RoomForm(request.POST, instance=room)
        # If the form is valid, save the data to the database and redirect to the home page
        if form.is_valid():
            form.save()
            return redirect('home')
    # Creates a dictionary context containing the form. This data will be passed to the template for rendering.
    context = {'form' : form}
    # Uses the render function to render the "base/room_form.html" template with the provided context.
    return render(request, 'base/room_form.html', context)
    
# Function for deleting rooms.
# Retrieves a room for deletion, deletes it from the database on a POST request, 
# and redirects to the home page. Otherwise, renders a confirmation page for deletion 
def deleteRoom(request, pk):
    # Retrieves a specific room based on the provided pk.
    room = Room.objects.get(id=pk)
    # Checks if the request method is POST.
    if request.method == 'POST':
        # Removes room from database, deletes it 
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})