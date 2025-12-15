#!/usr/bin/env python
"""复制截图文件到 Django 项目目录"""
import shutil
from pathlib import Path

# 源目录（前端 public 目录）
SOURCE_DIR = Path(__file__).parent.parent / 'machine-screenshot-query' / 'public'
# 目标目录
TARGET_DIR = Path(__file__).parent / 'screenshots'

def copy_screenshots():
    if not SOURCE_DIR.exists():
        print(f'源目录不存在: {SOURCE_DIR}')
        return
    
    # 创建目标目录
    TARGET_DIR.mkdir(exist_ok=True)
    
    # 复制所有子目录（排除 vite.svg 等非截图文件）
    copied = 0
    for item in SOURCE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            dest = TARGET_DIR / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            copied += 1
            print(f'已复制: {item.name}')
    
    print(f'\n共复制 {copied} 个型号目录到 {TARGET_DIR}')

if __name__ == '__main__':
    copy_screenshots()
