from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileHistory(models.Model):
    user_id = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)
    username = models.CharField(max_length=30,default="username")
    domains = models.CharField(max_length=100)
    filters = models.BooleanField()
    date = models.DateTimeField(auto_now=True)
    class Meta():
        ordering = ["-date"]
