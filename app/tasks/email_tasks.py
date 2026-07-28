from app.core.celery import celery_app
from app.services.email_service import EmailService


@celery_app.task
def send_welcome_email(email: str):
    service = EmailService()
    service.send_welcome_email(email)
