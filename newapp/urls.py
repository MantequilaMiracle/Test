from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('pikabu/', views.pikabutake, name="pikabutake"),
]
