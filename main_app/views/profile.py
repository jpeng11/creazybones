from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(req):
    return HttpResponse('Welcome to Index!')

# def other(req, user_id):