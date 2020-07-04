from django.urls import path, include
from ..views import accounts
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', accounts.signup, name='signup'),
    # path('<int>:user_id>', profile.other,)
]