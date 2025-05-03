import pytest
from post.models import Comment

@pytest.mark.django_db
class TestCommentModel:
    def test_create_comment(self, sample_post, sample_user):
        comment = Comment.objects.create(
            post=sample_post,
            user=sample_user,
            text='Test comment'
        )
        assert comment.post == sample_post
        assert comment.user == sample_user
        assert comment.text == 'Test comment'
        assert comment.likes.count() == 0
        assert not comment.parent
        
    def test_reply_comment(self, sample_post, sample_user):
        parent = Comment.objects.create(
            post=sample_post,
            user=sample_user,
            text='Test text'
        )
        reply = Comment.objects.create(
            post=sample_post,
            user=sample_user,
            text='Test reply comment',
            parent=parent
        )
        assert reply.parent == parent
        assert reply in parent.replies.all()

    def test_comment_str(self, sample_post, sample_user):
        comment = Comment.objects.create(
            post=sample_post,
            user=sample_user,
            text='Test comment'
        )
        assert str(comment) == f"Comment by {sample_user.username} on post {sample_post.id}"