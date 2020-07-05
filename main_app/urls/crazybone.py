from django.urls import path
from ..views import crazybone

urlpatterns = [
    path('<int:cb_id>', crazybone.detail, name='cb_detail'),
    # path('<int>:user_id>', profile.other,)
]
