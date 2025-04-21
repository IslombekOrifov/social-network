from django.db import models
from django.contrib.auth.models import AbstractUser
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

    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username } - {self.email}"
    