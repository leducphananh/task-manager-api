# 🚀 Task Manager API - Command Reference

Tài liệu tổng hợp các câu lệnh cần thiết để khởi chạy ứng dụng và quản lý cơ sở dữ liệu (Alembic Migration).

---

## 🖥️ 1. Khởi chạy ứng dụng (Start Application)

Kích hoạt môi trường và chạy máy chủ **Uvicorn** ở chế độ tự động reload khi sửa code (development mode):

```bash
# 1. Kích hoạt môi trường ảo (.venv)
source .venv/bin/activate

# 2. Khởi chạy máy chủ API
uvicorn app.main:app --reload
```

> **Lưu ý:** Sau khi chạy thành công, truy cập tài liệu API interacive tại `http://localhost:8000/docs`.

---

## 🗄️ 2. Quản lý Cơ sở dữ liệu (Alembic Migrations)

Các lệnh thực thi khi có thay đổi trong cấu trúc Model (`app/models/`):

### ✨ Tạo file Migration mới

Tự động quét thay đổi giữa Model và Database để sinh ra script migration:

```bash
alembic revision --autogenerate -m "tên_mô_tả_thay_đổi"
# Ví dụ: alembic revision --autogenerate -m "create users and tasks tables"
```

### ⬆️ Cập nhật Database (Apply Migrations)

Đẩy toàn bộ các migration chưa chạy vào cơ sở dữ liệu PostgreSQL:

```bash
alembic upgrade head
```

### ⬇️ Khôi phục lại (Rollback Migrations)

```bash
# Khôi phục (lùi lại) đúng 1 phiên bản trước đó
alembic downgrade -1

# Khôi phục (lùi lại) 2 phiên bản
alembic downgrade -2

# Xóa sạch toàn bộ cấu trúc bảng, đưa DB về trạng thái ban đầu (Trống)
alembic downgrade base
```

### 🔍 Kiểm tra trạng thái Migration

Xem phiên bản hiện tại mà database đang sử dụng:

```bash
alembic current
```

---

## 📦 3. Quản lý Thư viện (Dependencies)

```bash
# Cài đặt toàn bộ thư viện từ file requirements.txt
pip install -r requirements.txt

# Cập nhật lại file requirements.txt sau khi cài thêm thư viện mới
pip freeze > requirements.txt
```

---

## 🐳 4. Khởi chạy với Docker Compose (Docker Commands)

Khởi chạy song song cả database PostgreSQL và máy chủ API chỉ bằng 1 câu lệnh (tự động chạy migration khi khởi động):

```bash
# Khởi chạy toàn bộ hệ thống dưới nền (detached mode)
docker compose up -d --build

# Xem log trực tiếp của các container
docker compose logs -f

# Dừng và xóa toàn bộ container
docker compose down

# Dừng và xóa luôn cả volume dữ liệu của PostgreSQL
docker compose down -v
```

