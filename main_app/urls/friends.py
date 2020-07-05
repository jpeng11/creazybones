from django.urls import path, include
from ..views import accounts

urlpatterns = [
    path('', friends.index, name='friends'),
]