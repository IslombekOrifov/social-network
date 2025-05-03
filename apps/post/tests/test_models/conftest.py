import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
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
    image = Image.new('RGB', (100, 100), color='red')
    image_file = BytesIO()
    image.save(image_file, 'JPEG')
    image_file.seek(0)
    return SimpleUploadedFile(
        name='test.jpg',
        content=image_file.read(),
        content_type='image/jpeg'
    )

@pytest.fixture
def sample_video():
    return SimpleUploadedFile(
        name='test.mp4',
        content=b'00000018667479706D70343200000000',
        content_type='video/mp4'
    )