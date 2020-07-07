from django.urls import path, include
from ..views import notifications

urlpatterns = [
    path('', notifications.index, name='notifications'),
    path('accept/<int:pk>/<str:noti_type>', notifications.acceptrequest, name='accept'),
    path('reject/<int:pk>/<str:noti_type>', notifications.rejectrequest, name='reject'),
]