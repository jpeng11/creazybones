from django.shortcuts import render
from django.http import HttpResponse
from .seed import crazybones

# Create your views here.
def home(req):
    return HttpResponse('Welcome to CrazyBones!')

def seed(req):
    # for cb in crazybones:
        # add to model and save
    pass
    