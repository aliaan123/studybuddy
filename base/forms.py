from django.forms import ModelForm
from .models import Room

# Model form for room class. 
# Creates a form (RoomForm) based on the Room model. 
# This form is used for creating new rooms in the application.
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']