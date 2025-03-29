from pydantic import BaseModel,Field
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime, timedelta



# Webhook configuration
class WebhookDestination(BaseModel):
    name: str
    url: str
    active: bool = True

WEBHOOK_DESTINATIONS = {
    "webhook_site": WebhookDestination(
        name="Webhook.site Test",
        url="https://webhook.site/04846f68-7539-4741-8c84-ad379e64fcd2",
        active=True
    )
}