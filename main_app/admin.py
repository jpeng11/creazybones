from django.contrib import admin
from .models import Crazybone, Profile, Comment, TradeRequest, FriendList, Notification, Battle, Cb_Profile
# Register your models here.

admin.site.register(Crazybone)
admin.site.register(Profile)
admin.site.register(Cb_Profile)
admin.site.register(Comment)
admin.site.register(TradeRequest)
admin.site.register(FriendList)
admin.site.register(Notification)
admin.site.register(Battle)
