from django.shortcuts import render
from ..seed import crazybones

# Create your views here.


def home(request):
    return render(request, 'home.html')


def seed(req):
    # for cb in crazybones:
    # add to model and save
    pass
