from django.urls import path

from . import views

urlpatterns = [
    path('',view=views.home,name='home'),
    path('room/<str:pk>',view=views.room,name='room')
]