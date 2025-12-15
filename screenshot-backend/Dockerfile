FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 启动时自动迁移数据库
CMD python manage.py migrate && python init_data.py && python manage.py runserver 0.0.0.0:8000
