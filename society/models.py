from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone


class Services(models.Model):
    id=models.AutoField(primary_key = True)
    service_type=models.CharField(max_length=100)
    service_category=models.CharField(max_length=200)
    description =models.CharField(max_length=300)
    price=models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Comment(models.Model):
    service = models.ForeignKey(Services, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    id=models.AutoField(primary_key = True)
    title= models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True, null=True) 
    longitude = models.FloatField(max_length=200)
    latitude = models.FloatField(max_length=200) 
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='rsvps', on_delete=models.CASCADE)
    attending = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Attending' if self.attending else 'Not Attending'}"
    

class Ad(models.Model):
    id=models.AutoField(primary_key = True)
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=100)  
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        
    def __str__(self):
        return self.title
    
class ForumComment(models.Model):
    forum = models.ForeignKey(Forum, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ForumReply(models.Model):
    comment = models.ForeignKey(ForumComment, related_name="replies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_urgent = models.BooleanField(default=False)

    def _str_(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} on {self.ad.title}"

#chat
class Room(models.Model):
    name = models.CharField(max_length=1000)
    def _str_(self):
        return self.name

class RoomMessage(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  
    def _str_(self):
        return self.value

class DriveFile(models.Model):
    name = models.CharField(max_length=255)
    file_id = models.CharField(max_length=255, unique=True)
    download_url = models.URLField()

    def __str__(self):
        return self.name

   


