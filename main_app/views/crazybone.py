from django.shortcuts import render
from ..models import Crazybone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def detail(req, cb_id):
    cb = Crazybone.objects.get(id=cb_id)
    return render(req, 'crazybone/detail.html', {'cb': cb})

# def other(req, user_id):