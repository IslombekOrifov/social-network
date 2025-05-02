import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from account.models import CustomUser

@pytest.fixture
def sample_image():
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
        content_type='image/jpeg'
    )

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123',
        'phone': '+998912345678',
        'middle_name': 'Testovich',
        'date_of_birth': '1999-01-01',
        'about': 'Test user bio'
    }

@pytest.fixture
def create_user(db, user_data):
    def make_user(**kwargs):
        data = user_data.copy()
        data.update(kwargs)
        return CustomUser.objects.create_user(**data)
    return make_user