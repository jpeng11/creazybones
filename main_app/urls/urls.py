from django.urls import path, include
from ..views import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', include('main_app.urls.profile')),
    # path('trades/', include('main_app.urls.trades')),
    # path('seed/', views.seed, name='seed'),
]
