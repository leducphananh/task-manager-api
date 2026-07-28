from app.tasks.email_tasks import send_welcome_email


class NotificationService:
    def send_welcome_notification(self, email: str):
        """Gửi thông báo chào mừng qua Email Service bằng địa chỉ email (chuỗi ký tự)."""
        send_welcome_email.delay(email=email)


notification_service = NotificationService()
