from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended user model"""
    phone = models.CharField('Phone', max_length=20, blank=True)
    department = models.CharField('Department', max_length=100, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class VideoUploadRecord(models.Model):
    """Video upload record"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads', verbose_name='User')
    brand = models.CharField('Brand', max_length=50)
    model = models.CharField('Model', max_length=100)
    title = models.CharField('Video Title', max_length=200)
    filename = models.CharField('Filename', max_length=255)
    file_path = models.CharField('File Path', max_length=500)
    created_at = models.DateTimeField('Upload Time', auto_now_add=True)

    class Meta:
        verbose_name = 'Video Upload'
        verbose_name_plural = 'Video Uploads'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class QueryLog(models.Model):
    """Query log"""
    MODE_CHOICES = [
        ('Error Code', 'Error Code'),
        ('Component IO Check', 'Component IO Check'),
        ('Video Tutorial', 'Video Tutorial'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='query_logs', verbose_name='User')
    mode = models.CharField('Mode', max_length=50, choices=MODE_CHOICES)
    brand = models.CharField('Brand', max_length=50, blank=True)
    keyword = models.CharField('Keyword', max_length=200, blank=True)
    created_at = models.DateTimeField('Query Time', auto_now_add=True)

    class Meta:
        verbose_name = 'Query Log'
        verbose_name_plural = 'Query Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.mode} - {self.created_at}"
