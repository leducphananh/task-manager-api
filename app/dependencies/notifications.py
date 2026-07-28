from typing import Annotated

from fastapi import Depends

from app.services.notification_service import (NotificationService,
                                               notification_service)


def get_notification_service() -> NotificationService:
    return notification_service


NotificationServiceDep = Annotated[
    NotificationService,
    Depends(get_notification_service),
]
