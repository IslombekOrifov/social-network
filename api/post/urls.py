from django.urls import path
from .views import (
    PostListCreateView, PostRUDView, PostLikeView,
    CommentListCreateView, CommentRUDView,
    CommentLikeView, TagListView, PostReportView,
    UserPostsView
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_lc'),
    path('posts/<int:id>/', PostRUDView.as_view(), name='post_rud'),
    path('posts/<int:id>/like/', PostLikeView.as_view(), name='post_like'),
    
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment_lc'),
    path('comments/<int:id>/', CommentRUDView.as_view(), name='comment_rud'),
    path('comments/<int:id>/like/', CommentLikeView.as_view(), name='comment_like'),
    
    path('tags/', TagListView.as_view(), name='tag-list'),
    
    path('posts/<int:post_id>/report/', PostReportView.as_view(), name='post_report'),
    
    path('users/<int:user_id>/posts/', UserPostsView.as_view(), name='user_posts'),
]