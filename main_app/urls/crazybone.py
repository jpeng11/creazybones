from django.urls import path
from ..views import crazybone

urlpatterns = [
    path('<int:cb_id>', crazybone.detail, name='cb_detail'),
    path('<int:cb_id>/comment', crazybone.add_comment, name='add_comment'),
    path('<int:cb_id>/comment/<int:pk>/remove/', crazybone.remove_comment, name='delete_comment'),
    path('comment/<int:pk>/update/', crazybone.CommentUpdate.as_view(), name='update_comment'),
]
