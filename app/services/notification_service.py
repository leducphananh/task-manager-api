from typing import Optional

from app.services.email_service import EmailService, email_service


class NotificationService:
    def __init__(
        self,
        email_service: Optional[EmailService] = email_service,
    ):
        self.email_service = email_service

    def send_welcome_notification(self, email: str):
        """Gửi thông báo chào mừng qua Email Service bằng địa chỉ email (chuỗi ký tự)."""
        if self.email_service:
            self.email_service.send_welcome_email(email=email)


notification_service = NotificationService()
