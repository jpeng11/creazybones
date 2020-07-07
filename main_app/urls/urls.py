from django.urls import path, include
from ..views import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', include('main_app.urls.profile')),
    path('accounts/', include('main_app.urls.accounts')),
    path('crazybone/', include('main_app.urls.crazybone')),
    path('trades/', include('main_app.urls.trades')),
    path('seed/', views.seed, name='seed'),
]
