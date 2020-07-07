from django.urls import path, include
from ..views import notifications

urlpatterns = [
    path('', notifications.index, name='notifications'),
    path('accept/<int:pk>', notifications.acceptrequest, name='accept'),
    path('reject/<int:pk>', notifications.rejectrequest, name='reject'),
]