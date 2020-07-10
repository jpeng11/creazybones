from django.shortcuts import render, redirect
from ..seed import crazybones, users
from ..models import Crazybone, Profile, FriendList, Comment, TradeRequest, Cb_Profile, Battle
from django.contrib.auth.models import User
from operator import attrgetter
from itertools import chain
import random


# Create your views here.


def home(request):
    user = request.user
    crazybones = Crazybone.objects.all()
    feed = None
    if user.username != '':
        friends = []
        friends1 = FriendList.objects.filter(user=user.profile)
        for friend in friends1:
            friends.append(friend.myId)
        friends2 = FriendList.objects.filter(myId=user.profile)
        for friend in friends2:
            friends.append(friend.user)
        trades1 = TradeRequest.objects.filter(
            user_from__in=friends).order_by('-date')[:10]
        trades2 = TradeRequest.objects.filter(
            user_to__in=friends).order_by('-date')[:10]
        comments = Comment.objects.filter(
            user__in=friends).order_by('-date')[:10]
        battles1 = Battle.objects.filter(challenger__in=friends).order_by('-date')[:10]
        battles2 = Battle.objects.filter(defender__in=friends).order_by('-date')[:10]
        feed = sorted(
            chain(comments, trades1, trades2, battles1, battles2),
            key=attrgetter('date')
        )
        seen = set()
        new_feed = []
        for obj in feed:
            if obj.date not in seen:
                new_feed.append(obj)
                seen.add(obj.date)
                print(obj.date, obj.get_type())
        

        return render(request, 'home.html', {'cbs': crazybones, 'feed': reversed(new_feed[:15])})
    print('feed: ', feed)
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
            if(rand_cb in new_profile.cb.all()):
                cb2P=Cb_Profile.objects.get(cb=rand_cb, profile=new_profile)
                cb2P.qty+=1
                cb2P.save()
            else:
                new_profile.cb.add(rand_cb)
    return redirect('/')
