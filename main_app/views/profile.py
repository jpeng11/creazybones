from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from ..models import Profile, Crazybone


@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_cb = user.profile.cb.all()
    all_cb = Crazybone.objects.all().order_by('id')

    return render(request,
                  'profile/detail.html', {
                      'user': user,
                      'user_cb': user_cb,
                      'all_cb': all_cb})


class profileUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
