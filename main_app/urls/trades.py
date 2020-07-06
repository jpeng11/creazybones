from django.urls import path
from ..views import trades

urlpatterns = [
    path('', trades.index, name='trade'),
    path('result/', trades.result, name='trade-result'),
    path('tradecreate/', trades.create, name='trade-create'),
    # path('<int>:user_id>', profile.other,)
]
