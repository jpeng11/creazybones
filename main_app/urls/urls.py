from django.urls import path, include
from ..views import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', include('main_app.urls.profile')),
    path('accounts/', include('main_app.urls.accounts')),
    path('friends/', include('main_app.urls.friends')),
    path('notifications/', include('main_app.urls.notifications')),
    path('crazybone/', include('main_app.urls.crazybone')),
    path('trades/', include('main_app.urls.trades')),
    path('clan/', include('main_app.urls.clan')),
    path('seed/', views.seed, name='seed'),
]
