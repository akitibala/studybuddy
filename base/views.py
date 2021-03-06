from django.shortcuts import redirect, render , HttpResponse
# from django.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


from .models import Room ,Topic,Message
from .forms import RoomForm, UserForm
from django.db.models import Q
# rooms=[
#     {'id':1,'name':'Room 1'},
#     {'id':2 , 'name':'Room 2'},
# ]
# Create your views here.
def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        username = request.POST.get('username').lower()
        pwd = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        # return 
        user = authenticate(request,username=username,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Credentials does not match.')


    context={'page':page}
    return render(request,'base/login_register.html',context)

def logout_page(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error ocuured during during user creation')

    context={'form':form}
    return render(request,'base/login_register.html',context)

def user_profile(request,pk):
    user = User.objects.get(id=int(pk))
    room_msg=user.message_set.all()
    rooms=user.room_set.all()
    topics = Topic.objects.all()
    context={'user':user,'room_msg':room_msg,'rooms':rooms,'topics':topics}
    return render(request,'base/user_profile.html',context)

def home(request):
    q = request.GET.get('q','')
    # print(q)
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
    Q(name__icontains=q)|
    Q(description__icontains=q))
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_msg = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = { 'rooms':rooms,'topics':topics,'room_count':room_count,'room_msg':room_msg}
    return render(request,'base/home.html',context)

def  room(request,pk):
    room = Room.objects.get(id=int(pk))
    room_msg = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        # message.
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
        # room
    context ={'room':room,'room_msg':room_msg,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room =form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    
    context ={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('you are not allowed here!')
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name'),
        room.topic=topic,
        room.description=request.POST.get('description'),
        room.save()

        # form = RoomForm(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    # context ={'form':form}
    context ={'form':form,'topics':topics}

    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed here!')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context ={'obj':room}
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed here!')
    if request.method == "POST":
        message.delete()
        return redirect('home')
    context ={'obj':message}
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def update_user(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context={'form':form}
    return render(request,'base/update_user.html',context)
def topic_page(request):
    topics = Topic.objects.all()
    return render(request,'base/home.html',{'topics':topics})
# def activity_page(request):
#     return render(request,'base/room.html',{})
