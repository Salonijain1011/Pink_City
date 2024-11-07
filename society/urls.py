from django.urls import include, path
from society.Controller import AdController, AuthController, EventController, ForumController, MessageController, NotificationController, ServicesController
from society import views 
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('dashboard/', views.user_dashboard, name='user_dashboard'),
   path('upload/', views.upload, name='upload'),
   path('files/', views.file_list, name='file_list'),

    path("auth/login/", LoginView.as_view(template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('', views.home, name='home'),
    path("register/", AuthController.register, name='register'),
    path("login/", AuthController.user_login, name="login"),
    path("logout/", AuthController.user_logout, name='logout'),
    
    path('forum/', ForumController.forum, name='forum'),
    path('create_post/', ForumController.create_post, name='create_post'),
    path('forum/edit/<int:post_id>/', ForumController.edit_post, name='edit_post'),
    path('forum/delete/<int:post_id>/', ForumController.delete_post, name='delete_post'),
    path('forum/<int:post_id>/', ForumController.forum_detail, name='forum_detail'),

    path('events/', EventController.events, name='events'),
    path('create_event/', EventController.create_event, name='create_event'),
    path('events/edit/<int:event_id>/', EventController.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', EventController.delete_event, name='delete_event'),
    path('rsvp/<int:event_id>/', EventController.rsvp, name='rsvp'),

    path('services/', ServicesController.services, name='services'),
    path('post_service/', ServicesController.post_service, name='post_service'),
    path('services/edit/<int:service_id>/', ServicesController.edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', ServicesController.delete_service, name='delete_service'),
    path('service/<int:service_id>/', ServicesController.service_detail, name='service_detail'),

    path('classified/', AdController.classified, name='classified'),
    path('create_ad/', AdController.create_ad, name='create_ad'),
    path('classified/edit/<int:ad_id>/', AdController.edit_ad, name='edit_ad'),
    path('classified/delete/<int:ad_id>/', AdController.delete_ad, name='delete_ad'),
    path('message_seller/<int:ad_id>/', MessageController.message_seller, name='message_seller'),
    path('messages/', MessageController.messages, name='messages'),

    path('create-notification/', NotificationController.create_notification, name='create_notification'),
    path('notifications/', NotificationController.notification_list, name='notification_list'),
    path('notifications/', NotificationController.notifications_view, name='notifications_view'),
    path('notifications/delete/<int:notification_id>/', NotificationController.delete_notification, name='delete_notification'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('chatpage', views.chatpage, name='chatpage'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
