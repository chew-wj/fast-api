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
    "inventory": WebhookDestination(
        name="Inventory System",
        url="https://example.com/inventory-webhook"
    ),
    "notifications": WebhookDestination(
        name="Notification Service",
        url="https://example.com/notifications"
    )
}