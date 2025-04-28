from django.db import models

from account.models import CustomUser
from .services import upload_post_path


class Post(models.Model):
    POST_TYPE_TEXT = 'text'
    POST_TYPE_IMAGE = 'image'
    POST_TYPE_VIDEO = 'video'
    POST_TYPE_POLL = 'poll'
    POST_TYPE_REPOST = 'repost'
    
    POST_TYPE_CHOICES = [
        (POST_TYPE_TEXT, 'Текст'),
        (POST_TYPE_IMAGE, 'Изображение'),
        (POST_TYPE_VIDEO, 'Видео'),
        (POST_TYPE_POLL, 'Опрос'), 
        (POST_TYPE_REPOST, 'Репост'),
    ]

    content = models.TextField(blank=True, null=True, verbose_name="Текст поста")
    post_type = models.CharField(
        max_length=10, 
        choices=POST_TYPE_CHOICES, 
        default=POST_TYPE_TEXT,
        verbose_name="Тип поста"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        CustomUser, 
        related_name='liked_posts', 
        blank=True,
        verbose_name="Лайки"
    )
    is_archive = models.BooleanField(default=False, verbose_name="В архиве")
    is_banned = models.BooleanField(default=False, verbose_name="Заблокирован")
    owner = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name="Автор"
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    mentions = models.ManyToManyField(
        CustomUser, 
        blank=True, 
        related_name='mentioned_in_posts'
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    original_post = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reposts'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        indexes = [
            models.Index(fields=['owner', 'created_at']),
            models.Index(fields=['is_archive', 'is_banned']),
        ]

    def __str__(self):
        return f"{self.owner.username} - {self.post_type} post ({self.id})"

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()
    

class PostMedia(models.Model):
    """Model for saving post's media files"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='media_files',
        verbose_name="Пост"
    )
    file = models.FileField(
        upload_to=upload_post_path,
        verbose_name="Файл"
    )
    is_video = models.BooleanField(default=False, verbose_name="Это видео?")
    order = models.PositiveSmallIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='post_thumbs/', null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    duration = models.FloatField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Медиа файл поста"
        verbose_name_plural = "Медиа файлы постов"

    def __str__(self):
        return f"Media for post {self.post.id}"

    def save(self, *args, **kwargs):
        if not self.is_video and self.file:
            from PIL import Image
            img = Image.open(self.file)
            self.width, self.height = img.size
        super().save(*args, **kwargs)
        
        
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='replies'
    )
    likes = models.ManyToManyField(
        CustomUser, 
        related_name='liked_comments', 
        blank=True
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class PostReport(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Жалоба на пост"
        verbose_name_plural = "Жалобы на посты"
        unique_together = ('post', 'reporter')

    def __str__(self):
        return f"Report on post {self.post.id} by {self.reporter.username}"