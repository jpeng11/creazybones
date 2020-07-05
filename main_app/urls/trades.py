from django.urls import path
from ..views import trades

urlpatterns = [
    path('', trades.index, name='trade'),
    # path('<int>:user_id>', profile.other,)
]
