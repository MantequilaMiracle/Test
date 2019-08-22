from django import forms
from django.contrib.auth.models import User

class PostForm(forms.Form):
    public1 = forms.CharField(label="First public", max_length = 30, widget=forms.TextInput(attrs={
    "placeholder": " Vk public domain",
    "class": "form-control"
    }))
    public2 = forms.CharField(required=False, label="one more public", max_length = 30, widget=forms.TextInput(attrs={
    "placeholder": " Vk public domain",
    "class": "form-control"
    }))
    public3 = forms.CharField(required=False, label="one more public", max_length = 30, widget=forms.TextInput(attrs={
    "placeholder": " Vk public domain",
    "class": "form-control"
    }))
    today_posts = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
