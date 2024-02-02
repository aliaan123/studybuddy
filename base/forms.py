from django.forms import ModelForm
from .models import Room

# Model form for room class
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'