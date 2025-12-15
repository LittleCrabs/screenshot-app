from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """扩展用户模型"""
    phone = models.CharField('手机号', max_length=20, blank=True)
    department = models.CharField('部门', max_length=100, blank=True)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.username
