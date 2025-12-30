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


class VideoUploadRecord(models.Model):
    """视频上传记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads', verbose_name='用户')
    brand = models.CharField('品牌', max_length=50)
    model = models.CharField('型号', max_length=100)
    title = models.CharField('视频标题', max_length=200)
    filename = models.CharField('文件名', max_length=255)
    file_path = models.CharField('文件路径', max_length=500)
    created_at = models.DateTimeField('上传时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '视频上传记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class QueryLog(models.Model):
    """查询日志"""
    MODE_CHOICES = [
        ('Error Code', 'Error Code'),
        ('Component IO Check', 'Component IO Check'),
        ('Video Tutorial', 'Video Tutorial'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='query_logs', verbose_name='用户')
    mode = models.CharField('模式', max_length=50, choices=MODE_CHOICES)
    brand = models.CharField('品牌', max_length=50, blank=True)
    keyword = models.CharField('关键词', max_length=200, blank=True)
    created_at = models.DateTimeField('查询时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '查询日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.mode} - {self.created_at}"
