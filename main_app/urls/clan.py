from django.urls import path
from ..views import clan

urlpatterns = [
    path('', clan.index, name='clan_index'),
    
]