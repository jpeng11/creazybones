from django.urls import path
from ..views import battle

urlpatterns = [
    path('', battle.index, name='battle_index'),
    path('<int:battle_id>', battle.battle, name='battle'),
    path('result/', battle.result, name='battle_req_result'),
    path('create/', battle.create, name='battle_create')
]