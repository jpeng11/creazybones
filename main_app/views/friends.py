from django.shortcuts import render
from django.db.models import Q
from ..models import FriendList, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(req):
    # loggedin_user = Profile.objects.get(user = req.user)
    friends = FriendList.objects.filter(myId = Profile.objects.get(user=req.user))
    return render(req, 'friends/friends.html', {'friends': friends})