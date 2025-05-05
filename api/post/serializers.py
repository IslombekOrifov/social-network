from rest_framework import serializers

from post.models import Post, PostMedia, Tag, Comment, PostReport
from api.account.serializers import UserShortSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'usage_count']


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = [
            'id', 'file', 'is_video', 'order', 'thumbnail', 'caption',
            'duration', 'width', 'height'
        ]
        read_only_fields = ['thumbnail', 'width', 'height', 'duration']


class CommentSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'like_count', 'is_liked', 'parent']
        read_only_fields = ['user', 'created_at']
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exist()
        return False


class PostSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer(read_only=True)
    media_files = PostMediaSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'content', 'post_type', 'created_at',
            'updated_at', 'like_count', 'is_archive', 'is_banned',
            'media_files', 'tags', 'location', 'view_count',
            'comment_count', 'is_liked', 'is_owner', 'original_post'
        ]
        read_only_fields = [
            'owner', 'ceated_at', 'updated_at', 'like_count',
            'view_count', 'comment_count', 'is_liked', 'is_owner'
        ]
    
    def get_like_count(self, obj):
        return obj.like.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.owner


class PostCreateSerializer(serializers.ModelSerializer):
    media_files = serializers.ListSerializer(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    tags = serializers.ListSerializer(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'content', 'post_type', 'media_files', 
            'tags', 'location', 'original_post'
        ]
    
    def create(self, validated_data):
        media_files = validated_data.pop('media_files', [])
        tags = validated_data.pop('tags', [])
        
        post = Post.objects.create(**validated_data)
        
        for i, file in enumerate(media_files):
            is_video = file.content_type.startswith('video/')
            PostMedia.objects.create(post=post, file=file, is_video=is_video, order=i)
            
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name.lower())
            post.tags.add(tag)
        return post


class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = [
            'id', 'post', 'reason', 'created_at', 'is_resolved'
        ]
        read_only_fields = ['id', 'created_at', 'is_resolved']