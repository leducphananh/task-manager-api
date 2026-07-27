# Sử dụng Python 3.11 bản slim nhẹ nhàng, tối ưu hóa kích thước image
FROM python:3.11-slim

# Thiết lập biến môi trường
# PYTHONDONTWRITEBYTECODE=1: Không sinh ra file .pyc
# PYTHONUNBUFFERED=1: In log ra stdout ngay lập tức không qua bộ nhớ đệm
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Cài đặt các system dependencies cần thiết cho việc dịch và chạy một số thư viện Python (như psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy riêng file requirements vào trước để tận dụng cơ chế Docker cache cho bước pip install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn ứng dụng vào container
COPY . .

# Mở cổng 8000
EXPOSE 8000

# Lệnh khởi chạy:
# 1. Chạy Alembic upgrade head để đảm bảo schema database luôn được cập nhật mới nhất
# 2. Khởi chạy Uvicorn server trên host 0.0.0.0
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
