from django import forms
from django.contrib.auth.models import User

class PostForm(forms.Form):
    public = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={"placeholder": " Vk public domain", "class": "row-1"}))
    today_posts = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
    offset = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder":" default is 0", "class": "row-2"}))
    count = forms.IntegerField(required=False, min_value=0, max_value=100, widget=forms.NumberInput(attrs={"placeholder":" default is 10", "class": "row-3"}))
