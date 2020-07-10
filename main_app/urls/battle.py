from django.urls import path
from ..views import battle

urlpatterns = [
    path('', battle.index, name='battle_index'),
    path('<int:battle_id>', battle.battle, name='battle'),
    path('accept/<int:pk>/<str:noti_type>', battle.accept, name='battle_accept'),
    path('reject/<int:pk>/<str:noti_type>', battle.reject, name='battle_reject'),
    path('<int:battle_id>/error', battle.error, name='battle_error'),
    path('display/<int:battle_id>', battle.display, name='battle_display'),
    path('notif/<int:notif_id>', battle.notification, name='battle_notification'),
    path('<int:battle_id>/move/', battle.move, name='battle_move'),
    path('result/', battle.result, name='battle_req_result'),
    path('create/', battle.create, name='battle_create'),
]