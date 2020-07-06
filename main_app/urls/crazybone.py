from django.urls import path
from ..views import crazybone

urlpatterns = [
    path('<int:cb_id>', crazybone.detail, name='cb_detail'),
    path('<int:cb_id>/comment', crazybone.add_comment, name='add_comment'),
    path('<int:cb_id>/comment/<int:comment_id>/remove/', crazybone.remove_comment, name='remove_comment'),
    path('<int:cb_id>/comment/<int:comment_id>/update/', crazybone.update_comment, name='update_comment'),
]
