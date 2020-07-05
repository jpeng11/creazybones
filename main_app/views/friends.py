from django.shortcuts import render
from ..models import FriendList, Profile
from django.contrib.auth.decorators import login_required

@login_required
def index(req):
    