from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..models import FriendList, Profile, Notification

@login_required
def index(req):
    my_notif = Notification.objects.filter(noti_to = req.user.profile)
    return render(req, 'notification/notification.html', {'my_notif': my_notif})

@login_required
def acceptrequest(req, pk):
    return HttpResponse("Accepted request")

def rejectrequest(req, pk):
    return HttpResponse("Rejected request")