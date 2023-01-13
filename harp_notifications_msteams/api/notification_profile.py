from logger.logging import service_logger
import traceback
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import harp_notifications_msteams.settings as settings
from harp_notifications_msteams.logic.notification_processor import NotificationProcessor
from typing import Optional

log = service_logger()

router = APIRouter(prefix=settings.URL_PREFIX)


class TeamsNotification(BaseModel):
    teams_webhook: str
    title: str
    text: Optional[str]
    button_url: Optional[dict]
    facts: Optional[dict]


@router.post('/notifications/teams')
async def create_new_order(row_data: TeamsNotification):
    """
    Create new notification
    """

    data = row_data.dict()

    log.info(msg=f"Receive request to send Teams notification:\n{data}")

    try:
        processor = NotificationProcessor(teams_webhook=data['teams_webhook'])
        processor.send_notification(
            title=data['title'],
            text=data['text'],
            button_url=data['button_url'],
            facts=data['facts']
        )

        return 'Notification has been sent'
    except Exception as err:
        log.error(msg=f"Can`t process event\nERROR: {err}\nStack: {traceback.format_exc()}")

        raise HTTPException(status_code=500, detail=f"Backend error: {err}")
