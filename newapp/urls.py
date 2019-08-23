from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('posts/', views.multipost, name="posts"),
    path('accounts/<username>/profile/', views.profile, name="profile"),
    path('register/', views.registerview, name="register"),
]
