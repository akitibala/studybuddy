from django.shortcuts import redirect, render , HttpResponse
from .models import Room ,Topic
from .forms import RoomForm
from django.db.models import Q
# rooms=[
#     {'id':1,'name':'Room 1'},
#     {'id':2 , 'name':'Room 2'},
# ]
# Create your views here.
def home(request):
    q = request.GET.get('q','')
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
    Q(name__icontains=q)|
    Q(description__icontains=q))
    topics = Topic.objects.all()
    context = { 'rooms':rooms,'topics':topics}
    return render(request,'base/home.html',context)
def  room(request,pk):
    room = Room.objects.get(id=int(pk))
    
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

def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context ={'obj':room}
    return render(request,'base/delete.html',context)