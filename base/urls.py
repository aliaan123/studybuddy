from django.urls import path
from . import views

# Associates URLs with corresponding view functions. For example, an empty path leads to the home function, 
# "room/str:pk/" leads to the room function, and "create-room/" leads to createRoom.
urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerPage, name = "register"),

    
    path("", views.home, name = "home"),
    path("room/<str:pk>/", views.room, name = "room"),
    
    path('create-room/', views.createRoom, name = "create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name = "update-room"), 
    path('delete-room/<str:pk>/', views.deleteRoom, name = "delete-room"),# the url patterns, associate URLS like delete-room/3/ with corresponding functions, in this case the delete function. Calls it and with the pk of the room. 

    
]
