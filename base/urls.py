from django.urls import path
from . import views

# Associates URLs with corresponding view functions. For example, an empty path leads to the home function, 
# "room/str:pk/" leads to the room function, and "create-room/" leads to createRoom.
urlpatterns = [
    path("", views.home, name = "home"),
    path("room/<str:pk>/", views.room, name = "room"),
    path('create-room/', views.createRoom, name = "create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name = "update-room"),

    
]
