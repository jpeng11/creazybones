from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from ..models import Crazybone, Comment, Profile, Clan
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

def index(req):
    clans = Clan.objects.all()[:10]
    return render(req, 'clan/index.html', {'clans': clans})