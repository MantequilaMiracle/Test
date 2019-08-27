from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileHistory(models.Model):
    history = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)
    domains = models.CharField(max_length=100)
    filters = models.BooleanField()
    date = models.DateField(auto_now=True)
    class Meta():
        ordering = ["date"]
