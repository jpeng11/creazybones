from django.urls import path
from ..views import trades

urlpatterns = [
    path('', trades.index, name='trade'),
    path('result/', trades.result, name='trade-result'),
    path('create/', trades.create, name='trade-create'),
    path('user/', trades.user, name='trade-user'),
    path('action/', trades.action, name='trade-action')
]
