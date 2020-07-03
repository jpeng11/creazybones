from django.urls import path
from ..views import profile

urlpatterns = [
    path('', profile.index, name='profile'),
    # path('<int>:user_id>', profile.other,)
]
