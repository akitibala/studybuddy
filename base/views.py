from django.shortcuts import render , HttpResponse
# from django.

# Create your views here.
def home(request):
    return render(request,'base/home.html')
def  room(request):
    return render(request,'base/room.html')