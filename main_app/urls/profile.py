from django.urls import path
from ..views import profile

urlpatterns = [
    path('<int:user_id>/', profile.user_profile, name="user_detail"),
    path('<int:pk>/update/',
         profile.profileUpdate.as_view(), name="user_update"),
    path('<int:user_id>/add_photo', profile.add_photo, name="add_photo")
]
