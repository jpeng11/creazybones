from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from ..models import Crazybone, Comment, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Create your views here.
@login_required
def detail(req, cb_id):
    cb = Crazybone.objects.get(id=cb_id)
    comments = Comment.objects.filter(cb=cb_id)
    users_with_cb = Profile.objects.filter(cb=cb)
    print(users_with_cb)
    return render(req, 'crazybone/detail.html', {'cb': cb, 'comments': comments,'users_with_cb': users_with_cb})

@login_required
def add_comment(req, cb_id):
    text = req.POST.get('text')
    try:
        # user_profile = User.objects.get(id=req.user.id)
        cb=Crazybone.objects.get(id=cb_id)
        comment = Comment.objects.create(text=text, user=req.user.profile, cb=cb)
    except ValueError as e:
        print(e)
        print('no user found')
    return redirect('cb_detail', cb_id)

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['text']

@login_required
def remove_comment(req, cb_id, pk):
    Comment.objects.get(id=pk).delete()
    print('hello')
    return redirect(f'/crazybone/{cb_id}')
