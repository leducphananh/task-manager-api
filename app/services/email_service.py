class EmailService:
    def send_welcome_email(self, email: str):
        """Gửi email chào mừng tới người dùng vừa đăng ký."""
        print(f"Send welcome email to {email}")


email_service = EmailService()
