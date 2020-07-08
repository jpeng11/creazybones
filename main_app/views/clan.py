from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from ..models import Clan
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


@login_required
def index(req):
    clans = Clan.objects.all()[:10]
    return render(req, 'clan/index.html', {'clans': clans})


@login_required
def detail(req, clan_id):
    current_user = req.user
    clan = Clan.objects.get(id=clan_id)
    user_without_clan = User.objects.filter(profile__clan=None)
    return render(req, 'clan/detail.html', {'clan': clan, 'current_user': current_user, 'user_without_clan': user_without_clan})


class ClanCreate(LoginRequiredMixin, CreateView):
    model = Clan
    fields = ['name']
    success_url = '/clan/'


@login_required
def join(req, clan_id):
    clan = Clan.objects.get(id=clan_id)
    clan.members.add(req.user.profile)
    return redirect(f'/clan/{clan_id}')


@login_required
def add_new_member(req, clan_id):
    selected_user = req.POST['selected']
    clan = Clan.objects.get(id=clan_id)
    clan.members.add(User.objects.get(username=selected_user).profile)
    return redirect(f'/clan/{clan_id}')
