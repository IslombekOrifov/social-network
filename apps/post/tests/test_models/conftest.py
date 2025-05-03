import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from account.models import CustomUser
from post.models import Post

@pytest.fixture
def sample_user(db):
    return CustomUser.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpassword12345',
        phone='+998901234567'
    )

@pytest.fixture
def sample_post(db, sample_user):
    return Post.objects.create(
        content='Test content',
        owner=sample_user,
        post_type=Post.POST_TYPE_TEXT
    )

@pytest.fixture
def sample_image():
    return SimpleUploadedFile(
        name='test.jpg',
        content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
        content_type='image/jpeg'
    )

@pytest.fixture
def sample_video():
    return SimpleUploadedFile(
        name='test.mp4',
        content=b'\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00',
        content_type='video/mp4'
    )