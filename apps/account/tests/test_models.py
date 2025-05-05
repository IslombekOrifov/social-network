import pytest
from django.core.exceptions import ValidationError
from account.models import CustomUser

@pytest.mark.django_db
class TestCustomUserModel:
    def test_create_user(self, create_user):
        user = create_user()
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('TestPass123')
        assert user.phone == '+998912345678'
        assert not user.is_verified
        assert not user.is_deleted
        assert not user.is_confirmed

    def test_phone_validation_success(self, create_user):
        valid_numbers = [
            ('ali', '+998912345678'),
            ('vali', '+998997654321')
        ]
        for username, number in valid_numbers:
            user = create_user(username=username, phone=number, password='testpass')
            assert user.phone == number

    def test_phone_validation_failure(self, create_user):
        invalid_numbers = [
            ('998912345678', "Телефон должен начинаться с +998"),
            ('+99891234567', "Длина телефона должна быть 13 символов"),
            ('+992912345678', "Код страны должен быть 998"),
            ('+abcdefghijk', "Телефон должен содержать только цифры"),
        ]
        
        for number, error_msg in invalid_numbers:
            with pytest.raises(ValidationError) as excinfo:
                user = CustomUser(
                    username=f'user_{number}' if number else 'user_empty',
                    email=f'test_{number}@test.com',
                    phone=number,
                    password='testpass'
                )
                user.full_clean()

    def test_user_str_method(self, create_user):
        user = create_user()
        assert str(user) == f"{user.username} - {user.email}"

    def test_photo_upload(self, create_user, sample_image):
        user = create_user(photo=sample_image)
        assert user.photo.name.startswith('account/test_image')
        assert 'jpg' in user.photo.name

    def test_optional_fields(self, create_user):
        user = create_user(
            middle_name='',
            photo=None,
            date_of_birth=None,
            about=''
        )
        print(user.photo)
        assert user.middle_name == ''
        assert not user.photo
        assert user.date_of_birth is None
        assert user.about == ''

    def test_default_values(self, create_user):
        user = create_user()
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.is_verified is False
        assert user.is_deleted is False


@pytest.mark.django_db
class TestCustomUserUniqueConstraints:
    def test_unique_username(self, create_user):
        create_user(username='uniqueuser')
        with pytest.raises(Exception):
            create_user(username='uniqueuser')

    def test_unique_email(self, create_user):
        create_user(email='unique@example.com')
        with pytest.raises(Exception):
            create_user(email='unique@example.com')

    def test_unique_phone(self, create_user):
        create_user(phone='+998912345678')
        with pytest.raises(Exception):
            create_user(phone='+998912345678')