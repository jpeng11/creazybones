from django.shortcuts import render, redirect
from ..models import Crazybone, Comment, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def detail(req, cb_id):
    cb = Crazybone.objects.get(id=cb_id)
    comments = Comment.objects.filter(cb=cb_id)
    return render(req, 'crazybone/detail.html', {'cb': cb, 'comments': comments})

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

@login_required
def remove_comment(req, cb_id, comment_id):
    pass

@login_required
def update_comment(req, cb_id, comment_id):
    pass