from django.db import models

# Create your models here.
class Wish(models.Model):
	wishText = models.CharField(max_length = 60)
	pubDate = models.DateTimeField(auto_now=True)


class Publics(models.Model):
	public_name = models.CharField(max_length=30)
	
