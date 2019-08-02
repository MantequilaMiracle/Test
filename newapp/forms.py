from django import forms

class PostForm(forms.Form):
    public = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={"placeholder": "Vk public domain"}))
    today_posts = forms.BooleanField(required=False)
    offset = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder":"default is 0" }))
    count = forms.IntegerField(required=False, min_value=0, max_value=100, widget=forms.NumberInput(attrs={"placeholder":"default is 10" }))
