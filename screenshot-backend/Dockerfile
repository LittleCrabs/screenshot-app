FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 启动时自动迁移数据库，使用 gunicorn 生产服务器
CMD python manage.py migrate && python init_data.py && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2 --timeout 600
