from django.contrib import admin
from .models import Crazybone, Profile, Comment, TradeRequest, FriendList
# Register your models here.

admin.site.register(Crazybone)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(TradeRequest)
admin.site.register(FriendList)
