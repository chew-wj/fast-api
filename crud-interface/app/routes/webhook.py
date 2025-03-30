from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import logging
from datetime import datetime
from models.webhook import WebhookEvent, WebhookStatus
import asyncio
import uuid

logger = logging.getLogger(__name__)
webhook = APIRouter(prefix="/webhook")

# In-memory storage for webhook events (replace with database in production)
webhook_events: Dict[str, WebhookEvent] = {}

async def process_webhook_event(event_id: str, payload: Dict[str, Any]):
    try:
        # Simulate processing delay
        await asyncio.sleep(2)
        
        # Update event status
        webhook_events[event_id].status = "processed"
        webhook_events[event_id].processed_at = datetime.utcnow()
        
        logger.info(f"Webhook event {event_id} processed successfully")
    except Exception as e:
        webhook_events[event_id].status = "failed"
        webhook_events[event_id].error = str(e)
        logger.error(f"Failed to process webhook event {event_id}: {str(e)}")
        raise

@webhook.post("/", response_model=WebhookStatus)
async def receive_webhook(background_tasks: BackgroundTasks, event: WebhookEvent):
    event_id = str(uuid.uuid4())
    event.id = event_id
    event.received_at = datetime.utcnow()
    event.status = "received"
    
    webhook_events[event_id] = event
    
    # Process webhook event in background
    background_tasks.add_task(process_webhook_event, event_id, event.payload)
    
    return WebhookStatus(
        id=event_id,
        status="received",
        received_at=event.received_at
    )

@webhook.get("/{event_id}", response_model=WebhookEvent)
async def get_webhook_status(event_id: str):
    if event_id not in webhook_events:
        raise HTTPException(status_code=404, detail="Webhook event not found")
    return webhook_events[event_id]

@webhook.get("/", response_model=List[WebhookEvent])
async def list_webhook_events():
    return list(webhook_events.values()) 