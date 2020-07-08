from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from ..models import Crazybone, Comment, Profile, Clan
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

@login_required
def index(req):
    clans = Clan.objects.all()[:10]
    return render(req, 'clan/index.html', {'clans': clans})

@login_required
def detail(req, clan_id):
    clan = Clan.objects.get(id=clan_id)
    return render(req, 'clan/detail.html', {'clan': clan})

class ClanCreate(LoginRequiredMixin, CreateView):
    model = Clan
    fields = ['name']
    success_url = '/clan/'

@login_required
def join(req, clan_id):
    clan = Clan.objects.get(id=clan_id)
    clan.members.add(req.user.profile)
    return redirect(f'/clan/{clan_id}')