#!/usr/bin/env python
"""初始化数据库和创建管理员账户"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        print('管理员账户创建成功: admin / admin123')
    else:
        print('管理员账户已存在')

if __name__ == '__main__':
    create_superuser()
