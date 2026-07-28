class CacheKeys:
    """Lớp tập trung quản lý các quy tắc đặt tên khóa (Key naming convention) cho Redis Cache."""

    @staticmethod
    def task(user_id: int, task_id: int) -> str:
        """Khóa cache cho một task cụ thể của user."""
        return f"task:{user_id}:{task_id}"

    @staticmethod
    def task_list(user_id: int, page: int = 1) -> str:
        """Khóa cache đơn giản cho danh sách task của user theo trang."""
        return f"tasks:user:{user_id}:page:{page}"

    @staticmethod
    def task_list_pattern(user_id: int) -> str:
        """Pattern dùng để xóa toàn bộ cache các trang trong danh sách task của user."""
        return f"tasks:user:{user_id}:*"
