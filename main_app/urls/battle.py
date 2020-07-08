from django.urls import path
from ..views import battle

urlpatterns = [
    path('', battle.index, name='battle_index'),
    path('<int:battle_id>', battle.battle, name='battle'),
    path('<int:battle_id>/accept', battle.accept, name='battle_accept'),
    path('<int:battle_id>/error', battle.error, name='battle_error'),
    path('<int:battle_id>/display/', battle.display, name='battle_display'),
    path('<int:battle_id>/move/', battle.move, name='battle_move'),
    path('result/', battle.result, name='battle_req_result'),
    path('create/', battle.create, name='battle_create'),
]