from asyncio import Event
import io
import json
from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from pink_city import settings
from society.models import Services
from .models import  Event, Room, RoomMessage
from django.contrib import messages
from .models import Forum 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Notification
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Ad
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from society.Controller.Checker import check_session
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from .models import DriveFile
import threading


@never_cache
@login_required(login_url='/login/')
def home(request):
    latest_notification = Notification.objects.order_by('-created_at').first()

    return render(request, 'home.html', {
        'latest_notification': latest_notification,'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN  # Add API key to context

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

#files
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_DRIVE_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"]
    )
    return build('drive', 'v3', credentials=credentials)

def link_file_to_drive(drive_file_url):
    try:
        file_id = drive_file_url.split('/')[-2] 
        service = get_drive_service()
        drive_file = service.files().get(fileId=file_id, fields='name').execute()
        
        DriveFile.objects.create(
            name=drive_file.get('name'),
            file_id=file_id,
            download_url=f"https://drive.google.com/uc?id={file_id}&export=download"
        )
        print(f"Successfully linked file: {drive_file.get('name')} with ID: {file_id}")
    except Exception as e:
        print(f"Error linking file: {str(e)}")

@check_session
@login_required
def upload(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST' and request.user.is_superuser:
        drive_file_url = request.POST.get('file_url')
        
        if drive_file_url:
            threading.Thread(target=link_file_to_drive, args=(drive_file_url,)).start()
            return redirect('file_list')  

        else:
            return render(request, 'link_drive_file.html', {'error': 'Please provide a valid file URL.'})   
    return render(request, 'link_drive_file.html')

@check_session
@login_required
def file_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    files = DriveFile.objects.all()
    context={'files': files}
    response = render(request, 'file_list.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'    
    return response





