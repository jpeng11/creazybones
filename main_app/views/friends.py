from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..models import FriendList, Profile, Notification

@login_required
def index(req):
    # loggedin_user = Profile.objects.get(user = req.user)
    search_value = req.GET.get('search_box', 'admin')
    try:
        friends_myId = FriendList.objects.filter(myId = req.user.profile)
        friends_user = FriendList.objects.filter(user = req.user.profile)
        friends = friends_myId.union(friends_user)
        searched_users = Profile.objects.filter(user__username__icontains = search_value)
        searched_users = searched_users.exclude(user__username = req.user.username)
        for friend in friends:
            searched_users = searched_users.exclude(user__username = friend.user.user.username)
            searched_users = searched_users.exclude(user__username = friend.myId.user.username)
        return render(req, 'friends/friends.html', {'friends': friends, 'searched_users': searched_users})
    except:
        return render(req, 'friends/friends.html')

@login_required
def addfriend(req, pk):
    alreadyRequested = Notification.objects.filter(noti_from=req.user.profile)
    # friends_myId = FriendList.objects.filter(myId = req.user.profile)
    # friends_user = FriendList.objects.filter(user = req.user.profile)
    addedFriend = Profile.objects.get(user__id = pk)
    for noti in alreadyRequested:
        if(noti.noti_to.id == addedFriend.id):
            return redirect('friends')
    
    Notification.objects.create(notification_type='F', noti_from=req.user.profile, noti_to=addedFriend)
    return redirect('friends')

# def search(req):
#     search_value = req.GET.get('search_box', '')
#     print(search_value)
#     try:
#         searched_users = Profile.objects.filter(user__username__icontains = search_value)
#         return redirect('friends', searched_users=searched_users)
#     except:
#         return redirect('friends')