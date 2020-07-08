from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from ..models import Profile, Crazybone


@login_required
def user_profile(request, user_id):
    current_user = request.user
    user_profile = User.objects.get(id=user_id)
    user_cb = user_profile.profile.cb.all()
    all_cb = Crazybone.objects.all().order_by('id')

    return render(request,
                  'profile/detail.html', {
                      'current_user': current_user,
                      'user_profile': user_profile,
                      'user_cb': user_cb,
                      'all_cb': all_cb})


class profileUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
