import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .validators import validate_phone


class Subscription(models.Model):
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        MUTED = 'muted', 'Muted'
        PENDING = 'pending', 'Pending'
    
    subscriber = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE, 
        related_name='subscriptions'
    )
    target_user = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE, 
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE
    )
    notify = models.BooleanField(default=True)

    class Meta:
        unique_together = ('subscriber', 'target_user')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        indexes = [
            models.Index(fields=['subscriber', 'status']),
            models.Index(fields=['target_user', 'status']),
        ]

    def __str__(self):
        return f'{self.subscriber} → {self.target_user} ({self.status})'


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

    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    def subscribe_to(self, user):
        if self.is_private:
            Subscription.objects.get_or_create(
                subscriber=self,
                target_user=user,
                status=Subscription.SubscriptionStatus.PENDING
            )
        else:
            Subscription.objects.get_or_create(
                subscriber=self,
                target_user=user
            )
            
    def get_subscribers(self):
        return CustomUser.objects.filter(
            subscribers__subscriber=self,
            subscribers__status=Subscription.SubscriptionStatus.ACTIVE
        )
    
    def get_subscriptions(self):
        return CustomUser.objects.filter(
            subscriptions__target_user=self,
            subscriptions__status=Subscription.SubscriptionStatus.ACTIVE
        )

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