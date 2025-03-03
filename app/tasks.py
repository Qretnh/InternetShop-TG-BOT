from celery import shared_task
from .bot.services.sender import send


@shared_task
def send_mailing_task(id: int,
                      message: str,
                      buttons=None):
    status = send(id, message, buttons)
    return status
