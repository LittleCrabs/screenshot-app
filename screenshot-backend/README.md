# 机器截图查询系统 - 后端

## 快速开始

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 4. 创建管理员账户
python init_data.py

# 5. 复制截图文件到 screenshots 目录
# 将 machine-screenshot-query/public 下的图片文件夹复制到 screenshots/

# 6. 启动服务
python manage.py runserver
```

## 管理后台

访问 http://localhost:8000/admin/
- 用户名: admin
- 密码: admin123

### Excel 批量导入用户

在管理后台 -> 用户管理 -> 点击"批量导入用户 (Excel)"

Excel 格式：
| A列(用户名) | B列(密码) | C列(手机号) | D列(部门) |
|------------|----------|------------|----------|
| user1      | pass123  | 13800138000| 技术部    |

## API 接口

- `POST /api/users/login/` - 登录
- `POST /api/users/logout/` - 退出
- `GET /api/users/info/` - 用户信息
- `GET /api/screenshots/models/` - 获取型号列表
- `GET /api/screenshots/versions/?model=xxx` - 获取版本列表
- `GET /api/screenshots/search/?model=xxx&keyword=xxx&version=xxx` - 搜索图片
