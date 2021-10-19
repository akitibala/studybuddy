from django.shortcuts import render , HttpResponse
from .models import Room
# from django.
# rooms=[
#     {'id':1,'name':'Room 1'},
#     {'id':2 , 'name':'Room 2'},
# ]
# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = { 'rooms':rooms}
    return render(request,'base/home.html',context)
def  room(request,pk):
    room = Room.objects.get(id=int(pk))
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room=i
    context ={'room':room}
    return render(request,'base/room.html',context)