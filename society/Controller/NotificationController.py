from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from pink_city import settings
from society.models import Notification
from society.forms import NotificationForm
from django.core.mail import send_mail
from society.Controller.Checker import check_session
from society.models import User  


# @check_session
# def create_notification(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     if request.method == 'POST':
#         form = NotificationForm(request.POST)
#         if form.is_valid():
#             notification = form.save(commit=False)
#             notification.user = request.user
#             notification.save()

#             if notification.is_urgent:
#                 users = User.objects.exclude(email__isnull=True).exclude(email='')  
#                 subject = notification.title
#                 message = notification.message

#                 for user in users:
#                     send_mail(
#                         subject=subject,
#                         message=message,
#                         from_email=settings.DEFAULT_FROM_EMAIL,
#                         recipient_list=[user.email],
#                         fail_silently=False,
#                     )

#             return redirect('home')
#     else:
#         form = NotificationForm()

#     context = {'form': form}
#     response = render(request, 'create_notification.html', context)
#     response['Cache-Control'] = 'no-store'
#     response['Pragma'] = 'no-cache'
#     response['Expires'] = '0'
#     return response



import threading
from django.core.mail import send_mail
from django.conf import settings

@check_session
def create_notification(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()

            if notification.is_urgent:
                threading.Thread(target=send_notification_emails, args=(notification,)).start()

            return redirect('home')
    else:
        form = NotificationForm()

    context = {'form': form}
    response = render(request, 'create_notification.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def send_notification_emails(notification):
    users = User.objects.exclude(email__isnull=True).exclude(email='')
    subject = notification.title
    message = notification.message

    for user in users:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


@check_session
def notification_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notifications = Notification.objects.all().order_by('-created_at')
    
    context = {'notifications': notifications}

    response = render(request, 'notification_list.html', context)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


def notifications_view(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return HttpResponseRedirect(reverse('notifications_view'))
