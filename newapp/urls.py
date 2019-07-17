from django.urls import path
from . import views

urlpatterns = [
    path('', views.newview, name="newview"),
]
