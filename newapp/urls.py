from django.urls import path
from . import views

urlpatterns = [
    path('', views.newview, name="newview"),
    path('pikabu/', views.pikabutake, name="pikabutake"),
    path('<int:pk>/delete/', views.deleterecord, name="deleterecord"),
]
