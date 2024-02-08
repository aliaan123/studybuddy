# Import necessary modules from Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm

# rooms = [
#    {"id":1, "name":"Lets learn python!"},
#    {"id":2, "name":"Design with me!"},
#    {"id":3, "name":"Frontend developers!"},
# ]

# Define views for the application


# Function for logging in a user
def loginPage(request):
    
    # sets the variable page to specify that this is a login page, it is passed into the context variable, and used in the html to run the correct code.
    page = 'login'
    
    # If the user is already logged in and tries to click on the login button again, they will just get redirected to home instead. 
    if request.user.is_authenticated:
        return redirect('home')
    
    # Checks if a POST request was sent. 
    if request.method == 'POST':
        # Get the username and password from the data sent in the POST request. 
        username = request.POST.get('username').lower()
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
                
    
    context = {'page' : page}
    return render(request, 'base/login_register.html', context)    

# Function for logging out a user. 
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    # else is used in the html, so no need for a page variable here. 
    form = UserCreationForm()
    
    # Check if method is a POST request
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # passes in the data: username and password into user creation form
        # Checks if the form is valid
        if form.is_valid():
            user = form.save(commit=False) # saving the form, freezing it in time. If the form is valid, the user is created and we want to be able to access it right away. This is why we set commit = False
            user.username = user.username.lower() # Now that the user is created, we can access their credentials, like username and password. We lowercase the username of the user. 
            user.save() # saves the user. 
            login(request, user) # logs the user in.
            return redirect('home') # sends the user back to the home page.
        else: 
            messages.error(request, 'An error occurred during registration')
            
    context = {'form' : form}
    return render(request,'base/login_register.html', context)


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
    # filters and only gets the messages for the room based on what topic it is   
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    # Creates a dictionary context containing the queried rooms and all topics. This data will be passed to the template for rendering.
    context = {"rooms" : rooms, 'topics': topics, 
               'room_count' : room_count, 'room_messages': room_messages}
    # Uses the render function to render the "base/home.html" template with the provided context.
    return render(request, "base/home.html", context)

#  Fetches a specific room based on the provided primary key (pk) from the URL. 
# The room is then passed to the "base/room.html" template.
def room(request, pk):
    # Retrieve a single room from the database based on the provided id (pk)
    room = Room.objects.get(id=pk) 
    
    # Queries child object of a specific room. If we take the parent model, in this case we have a room. 
    # To get all the children, all we have to do is specify the model name, in this case it is message. We put that in lowercase value (message).
    # So the model name in lowercase followed by "_set.all()". Which is basically saying, give us the set of messages that are related to this specific room.
    room_messages = room.message_set.all()

    # brings the participants in. all() method is used for the many to many relationship field to get all the participants. These are passed into the context dictionary.
    participants = room.participants.all()

    # Creates a Message object and sets the model fields.
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body') # The body is passed in from the comment form in the room.html, where in input : name = 'body'. Thats how we get that data.
        )
        # The user will be added to the many to many field for the participants, so that we can render out the participants of a chatroom.  
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    # Creates a dictionary context containing the retrieved room. This data will be passed to the template for rendering.
    context = {"room" : room, "room_messages" : room_messages, "participants" : participants}
    # Uses the render function to render the "base/room.html" template with the provided context.
    return render(request, "base/room.html", context)


# Handles the creation of a new room. It initializes a RoomForm, processes the form data on a POST request, 
# saves the room to the database if valid, and redirects to the home page.
@login_required(login_url='login') # Requires to be logged in, in order to create a room. Redirects user to login page if they are not logged in.
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
@login_required(login_url='login') # Requires to be logged in, in order to update a room. Redirects user to login page if they are not logged in.
def updateRoom(request, pk):
    # Retrieves a specific room based on the provided pk.
    room = Room.objects.get(id=pk)
    # Initializes a form instance with the existing room data (instance=room). 
    form = RoomForm(instance=room) # the form will be prefilled with the room value.
    
    # Only allows the owner of the room to update the room. 
    if request.user != room.host :
        return HttpResponse('You are not allowed here!')
    
    
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
@login_required(login_url='login') # Requires to be logged in, in order to delete a room. Redirects user to login page if they are not logged in.
def deleteRoom(request, pk):
    # Retrieves a specific room based on the provided pk.
    room = Room.objects.get(id=pk)
    
     # Only allows the owner of the room to delete the room. 
    if request.user != room.host :
        return HttpResponse('You are not allowed here!')
    
    # Checks if the request method is POST.
    if request.method == 'POST':
        # Removes room from database, deletes it 
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})



@login_required(login_url='login') # Requires to be logged in, in order to delete a message. Redirects user to login page if they are not logged in.
def deleteMessage(request, pk):
    # Retrieves a specific message based on the provided pk.
    message = Message.objects.get(id=pk)
    
     # Only allows the owner of the message to delete the message. 
    if request.user != message.user :
        return HttpResponse('You are not allowed here!')
    
    # Checks if the request method is POST.
    if request.method == 'POST':
        # Removes message from database, deletes it 
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})