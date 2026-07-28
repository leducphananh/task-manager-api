import redis

from app.core.config import settings

# Khởi tạo client kết nối tới Redis Server (Connection setup hạ tầng)
# decode_responses=True giúp tự động chuyển b'string' (bytes) sang 'string' bình thường
redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)
