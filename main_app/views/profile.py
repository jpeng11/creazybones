from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from ..models import Profile, Crazybone


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    # user_cb = User.objects.get(id=user_id).profile.cb.all()
    user_cb = user.profile.cb.all()
    all_cb = Crazybone.objects.all().order_by('id')
    # cb_user_doesnot_own = Crazybone.objects.exclude(
    #     id__in=user_cb.values_list('id'))

    return render(request, 
        'profile/detail.html', {
            'user': user, 
            'user_cb': user_cb, 
            #'cb_user_doesnot_own': cb_user_doesnot_own,
            'all_cb': all_cb})


class profileUpdate(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'email']
