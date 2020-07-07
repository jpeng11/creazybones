from django.urls import path
from ..views import clan

urlpatterns = [
    path('', clan.index, name='clan_index'),
    path('create/', clan.ClanCreate, name='clan_create')
]