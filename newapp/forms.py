from django.forms import ModelForm, TextInput
from .models import Wish

class WishForm(ModelForm):
    class Meta:
        model = Wish
        fields = ["wishText"]
        widgets = {"wishText": TextInput(attrs={"class": "form-control","placeholder": "Write a wish"})}
