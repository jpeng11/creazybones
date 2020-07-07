from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from ..models import Profile, Crazybone


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_cb = User.objects.get(id=user_id).profile.cb.all()
    crazybones = Crazybone.objects.all()
    return render(request, 'profile/detail.html', {'user': user, 'user_cb': user_cb, 'crazybones': crazybones})
