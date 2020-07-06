from django.shortcuts import render, redirect
from ..seed import crazybones, users
from ..models import Crazybone, Profile
from django.contrib.auth.models import User
import random

# Create your views here.


def home(request):
    crazybones = Crazybone.objects.all()
    return render(request, 'home.html', {'cbs': crazybones})


def seed(req):
    # delete old crazybones, profiles and users
    Crazybone.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()

    # add all the crazybones to the database
    cbs = crazybones()
    for ind, cb in enumerate(cbs):
        c = Crazybone.objects.create(
            name=cb['name'], img=cb['img'], description=cb['description'])

    # adds the users, creates a profile attached to it, then adds 10 random crazybones
    seed_users = users()
    for user in seed_users:
        new_user = User.objects.create(username=user['username'])
        new_profile = Profile.objects.create(user=new_user)
        for z in range(10):
            rand_cb = Crazybone.objects.order_by('?')[0]
            new_profile.cb.add(rand_cb)
    return redirect('/')
