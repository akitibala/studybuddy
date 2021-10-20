from django.shortcuts import redirect, render , HttpResponse
from .models import Room
from .forms import RoomForm
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

def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context ={'form':form}
    return render(request,'base/room_form.html',context)

def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context ={'form':form}
    return render(request,'base/room_form.html',context)