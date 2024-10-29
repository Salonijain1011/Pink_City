from .models import DriveFile, Event, Room, RoomMessage
from django.contrib import admin
from .models import Services
from .models import Forum
from .models import Ad

# Register your models here.
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_type','user','service_category', 'description', 'price')
    search_fields = ('service_type','user__username', 'service_category', 'description')
admin.site.register(Services, ServicesAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display=('title', 'user','date','location','description')
    search_fields=('title','user__username','location','description')
admin.site.register(Event,EventAdmin)

class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'description')  
    search_fields = ('title', 'user__username', 'description')
admin.site.register(Forum,ForumAdmin)

class AdAdmin(admin.ModelAdmin):
    list_display=('title','user','price','description')
    search_fields=('title','user__username','name','description')
admin.site.register(Ad,AdAdmin)


admin.site.register(Room)
admin.site.register(RoomMessage)
admin.site.register(DriveFile)


