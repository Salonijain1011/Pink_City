# from urllib import request
from asyncio import Event
import json
from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from society.models import Services
from .models import  Event, Room, RoomMessage
from django.contrib import messages
from .models import Forum 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from channels.layers import get_channel_layer
from django.template import RequestContext
from .models import Notification
from .forms import NotificationForm
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Ad, Message
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from society.Controller.Checker import check_session


@never_cache
@login_required(login_url='/login/')
def home(request):
    latest_notification = Notification.objects.order_by('-created_at').first()

    return render(request, 'home.html', {
        'latest_notification': latest_notification,
    })

@check_session
@login_required
def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_posts = Forum.objects.filter(user=request.user)
    user_events = Event.objects.filter(user=request.user)
    user_services = Services.objects.filter(user=request.user)
    user_ads = Ad.objects.filter(user=request.user)

    context = {
        'user_posts': user_posts,
        'user_events': user_events,
        'user_services': user_services,
        'user_ads': user_ads,
    }
    response = render(request, 'user_dashboard.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'    
    return response

#chat
@check_session
@login_required
def chatpage(request):
    response = render(request, 'chatpage.html')
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def room(request, room):
    username = request.GET.get('username', request.user.username)  
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

@login_required
def checkview(request):
    room = request.POST['room_name']
    username = request.user.username  

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    room = Room.objects.get(id=room_id)
    new_message = RoomMessage.objects.create(value=message, user=username, room=room)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = RoomMessage.objects.filter(room=room_details)
    return JsonResponse({"messages": list(messages.values())})


