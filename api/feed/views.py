from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from post.models import Post
from api.post.serializers import PostSerializer


class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        subscribed_users = user.get_subscriptions()

        queryset = Post.objects.filter(
            owner__in=subscribed_users,
            is_archive=False,
            is_banned=False
        ).select_related('owner').prefetch_related(
            'media_files', 'tags', 'likes'
        )

        post_type = self.request.query_params.get('type')
        if post_type:
            queryset = queryset.filter(post_type=post_type)
            
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context