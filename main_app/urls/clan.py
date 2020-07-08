from django.urls import path
from ..views import clan

urlpatterns = [
    path('', clan.index, name='clan_index'),
    path('<int:clan_id>', clan.detail, name='clan_detail'),
    path('create/', clan.ClanCreate.as_view(), name='clan_create'),
    path('<int:clan_id>/join', clan.join, name='clan_join'),
]