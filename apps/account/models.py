import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .validators import validate_phone


class CustomUser(AbstractUser):
    """ Custom user model """
    phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[validate_phone]
    )
    middle_name = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(
        upload_to='account/',
        blank=True, null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    about = models.CharField(max_length=300, blank=True)
    is_confirmed = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username } - {self.email}"


class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @classmethod
    def create_verification_code(cls, user):
        code = ''.join(random.choices(string.digits, k=6))
        cls.objects.filter(user=user).delete()
        expires_at = timezone.now() + timezone.timedelta(minutes=15)
        
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=expires_at
        )

    def is_valid(self):
        return timezone.now() < self.expires_at