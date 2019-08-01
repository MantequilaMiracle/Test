from django import forms

class PostForm(forms.Form):
    public = forms.CharField(label="write a domain", max_length = 30)
    today_posts = forms.BooleanField(required=False)
    offset = forms.IntegerField(min_value = 0)
    count = forms.IntegerField(min_value = 0, max_value = 100)
