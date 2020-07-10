from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..models import FriendList, Profile, Notification, TradeRequest



@login_required
def index(req):
    my_notif = Notification.objects.filter(noti_to = req.user.profile)
    return render(req, 'notification/notification.html', {'my_notif': my_notif})

@login_required
def acceptrequest(req, pk, noti_type):
    sent_from = Profile.objects.get(user__id = pk)
    sent_to = Profile.objects.get(user__id = req.user.id)
    if(noti_type == 'F'):
        try:
            FriendList.objects.create(user=sent_from, myId=sent_to)
            this_noti = Notification.objects.filter(noti_to = req.user.profile)
            this_noti = this_noti.filter(notification_type = noti_type)
            this_noti = this_noti.get(noti_from = sent_from)
            this_noti.delete()
            return redirect('notifications')
        except:
            return HttpResponse("Failed Request (Friend)")
    if(noti_type == 'T'):
        try:
            this_noti = Notification.objects.filter(noti_to = req.user.profile)
            this_noti = this_noti.filter(notification_type = noti_type)
            this_noti = this_noti.get(noti_from = sent_from)
            return redirect('trade-user')
        except:
            return HttpResponse("Failed Request (Trade)")
    return HttpResponse(f"Accepted request from profile id --> {sent_from}, {sent_to}")

def rejectrequest(req, pk, noti_type):
    if(noti_type == 'F'):
        try:
            this_noti = Notification.objects.filter(noti_to = req.user.profile)
            this_noti = this_noti.get(noti_from = Profile.objects.get(user__id = pk))
            this_noti.delete()
            return redirect('notifications')
        except:
            return HttpResponse("Failed")
    elif(noti_type == 'T'):
        try:
            this_noti = Notification.objects.filter(noti_to = req.user.profile)
            this_noti = this_noti.filter(notification_type = noti_type)
            this_noti = this_noti.get(noti_from = Profile.objects.get(user__id = pk))
            trade_request = TradeRequest.objects.get(created_notification = this_noti)
            trade_request.status = 'R'
            trade_request.save()
            this_noti.delete()
            return redirect('notifications')
        except:
            return HttpResponse("Failed")
    return HttpResponse(f"Rejected request from profile id --> {pk}, {noti_type}")