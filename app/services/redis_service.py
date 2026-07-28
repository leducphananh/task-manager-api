import json
from typing import Any, Optional, Type, TypeVar

import redis
from pydantic import BaseModel

from app.core.redis import redis_client

T = TypeVar("T", bound=BaseModel)


class RedisService:
    """Service điều phối các thao tác với bộ nhớ đệm Redis (hỗ trợ tự động chuyển đổi JSON & Pydantic)."""

    def __init__(self, client: redis.Redis = redis_client):
        self.client = client

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Lưu dữ liệu vào Redis. Tự động chuyển đổi Pydantic model, dict, list sang chuỗi JSON.

        Args:
            key (str): Tên khóa.
            value (Any): Giá trị (chuỗi, số, dict, list, hoặc Pydantic BaseModel).
            ex (Optional[int], optional): Thời gian hết hạn tính bằng giây. Defaults to None.
        Returns:
            bool: True nếu lưu thành công.
        """
        if isinstance(value, BaseModel):
            # Sử dụng model_dump_json() của Pydantic v2 để tự động xử lý datetime, enum...
            val_str = value.model_dump_json()
        elif isinstance(value, (dict, list)):
            val_str = json.dumps(value, ensure_ascii=False)
        elif isinstance(value, (int, float, bool)):
            val_str = str(value)
        else:
            val_str = str(value)

        return self.client.set(name=key, value=val_str, ex=ex)

    def get(self, key: str) -> Optional[str]:
        """Lấy giá trị chuỗi nguyên bản từ Redis theo key."""
        return self.client.get(name=key)

    def get_json(self, key: str) -> Optional[Any]:
        """Lấy giá trị từ Redis và tự động parse từ chuỗi JSON sang dict hoặc list."""
        data = self.get(key)
        if not data:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    def get_model(self, key: str, model_class: Type[T]) -> Optional[T]:
        """Lấy giá trị từ Redis và tự động convert sang object Pydantic model.

        Args:
            key (str): Tên khóa cần lấy.
            model_class (Type[T]): Class Pydantic mong muốn trả về (ví dụ: TaskResponse).
        Returns:
            Optional[T]: Object Pydantic nếu tìm thấy, ngược lại trả về None.
        """
        data = self.get(key)
        if not data:
            return None
        return model_class.model_validate_json(data)

    def delete(self, *keys: str) -> int:
        """Xóa một hoặc nhiều khóa khỏi Redis.

        Args:
            *keys (str): Danh sách khóa cần xóa.
        Returns:
            int: Số lượng khóa đã xóa thành công.
        """
        if not keys:
            return 0
        return self.client.delete(*keys)

    def delete_by_pattern(self, pattern: str) -> int:
        """Xóa tất cả các khóa khớp với pattern (ví dụ: tasks:1:*).

        Args:
            pattern (str): Mẫu chuỗi cần quét và xóa.
        Returns:
            int: Số lượng khóa đã tìm thấy và xóa thành công.
        """
        keys = self.client.keys(pattern)
        if not keys:
            return 0
        return self.client.delete(*keys)


# Tạo một instance duy nhất (Singleton) để sử dụng toàn ứng dụng
redis_service = RedisService()
