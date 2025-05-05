import pytest
from datetime import timedelta
from django.utils import timezone
from post.models import Post, PostMedia, Tag, Comment


@pytest.mark.django_db
class TestPostModel:
    def test_create_post(self, sample_post):
        assert sample_post.content == 'Test content'
        assert sample_post.post_type == Post.POST_TYPE_TEXT
        assert sample_post.like_count == 0
        assert sample_post.comment_count == 0
        assert not sample_post.is_archive
        assert not sample_post.is_banned

    def test_post_str(self, sample_post):
        assert str(sample_post) == f'{sample_post.owner.username} - text post ({sample_post.id})'

    def test_post_ordering(self,sample_user):
        post1 = Post.objects.create(
            content='Test post 1',
            owner=sample_user,
            post_type=Post.POST_TYPE_TEXT
        )
        post2 = Post.objects.create(
            content='Test post 2',
            owner=sample_user,
            post_type=Post.POST_TYPE_TEXT
        )
        posts =Post.objects.all()
        assert posts[0] == post2
        assert posts[1] == post1

    def test_post_types(self, sample_user):
        for post_type, _ in Post.POST_TYPE_CHOICES:
            post = Post.objects.create(
                content=f'{post_type} post',
                owner=sample_user,
                post_type=post_type
            )
            assert post.post_type == post_type

    def test_like_post(self, sample_post, sample_user):
        sample_post.likes.add(sample_user)
        assert sample_post.like_count == 1
        assert sample_user in sample_post.likes.all()

    def test_tags_post(self, sample_post):
        tag = Tag.objects.create(name='Test', slug='test')
        sample_post.tags.add(tag)
        assert sample_post.tags.count() == 1
        assert tag in sample_post.tags.all()

    def test_repost(self, sample_post, sample_user):
        repost = Post.objects.create(
            owner=sample_user,
            post_type=Post.POST_TYPE_REPOST,
            original_post=sample_post
        )
        assert repost.original_post == sample_post
        assert repost in sample_post.reposts.all()