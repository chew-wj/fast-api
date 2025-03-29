import httpx
import asyncio
from models.webhook import WEBHOOK_DESTINATIONS
import logging

logger = logging.getLogger(__name__)

async def send_webhook(event_type: str, payload: dict):
    """
    Send webhook notifications to all active destinations
    """
    async with httpx.AsyncClient() as client:
        tasks = []
        for dest in WEBHOOK_DESTINATIONS.values():
            if dest.active:
                tasks.append(
                    client.post(
                        dest.url,
                        json={
                            "event_type": event_type,
                            "payload": payload
                        }
                    )
                )
        
        if tasks:
            try:
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                for resp in responses:
                    if isinstance(resp, Exception):
                        logger.error(f"Webhook delivery failed: {str(resp)}")
                    else:
                        logger.info(f"Webhook delivered successfully: {resp.status_code}")
            except Exception as e:
                logger.error(f"Error sending webhooks: {str(e)}") 