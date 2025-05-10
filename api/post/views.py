from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework import permissions, status, generics, filters, serializers
from rest_framework.response import Response

from post.models import Post, PostMedia, Tag, Comment, PostReport
from .serializers import (
    PostCreateSerializer, PostSerializer, PostMediaSerializer,
    PostReportSerializer, TagSerializer, CommentSerializer
)
from api.account.serializers import UserShortSerializer
from account.permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_archive=False, is_banned=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'view_count', 'like_count']
    search_fields = ['content', 'tags__name', 'owner__username']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostRUDView(generics. RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            instance.view_count += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostLikeView(generics.GenericAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        post = self.get_queryset()
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return Response({'detail': 'unliked'})
        else:
            post.likes.add(request.user)
            return Response({'detail': 'liked'})


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id, parent__isnull=True)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(user=self.request.user, post=post)


class CommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'


class CommentLikeView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            return Response({'detail': 'unliked'})
        else:
            comment.likes.add(request.user)
            return Response({'detail': 'liked'})


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class PostReportView(generics.CreateAPIView):
    serializer_class = PostReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        if PostReport.objects.filter(post=post, reporter=self.request.user).exists():
            raise serializers.ValidationError("You have already reported this post")
        serializer.save(reporter=self.request.user, post=post)


class UserPostsView(generics.ListAPIView):
    serializer_class =PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(
            owner__id=user_id, 
            is_archive=False, 
            is_banned=False
        ).order_by('-created_at')