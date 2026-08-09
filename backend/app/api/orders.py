from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import ContactRequest
from app.schemas.schemas import ContactRequestResponse, ContactRequestCreate
from app.services.telegram import send_contact_request_alert

import re

router = APIRouter(tags=["Contact Requests"])

def normalize_telegram_username(val: str) -> str:
    cleaned = val.strip()
    if cleaned.startswith("https://t.me/"):
        cleaned = cleaned.replace("https://t.me/", "")
    elif cleaned.startswith("http://t.me/"):
        cleaned = cleaned.replace("http://t.me/", "")
    elif cleaned.startswith("t.me/"):
        cleaned = cleaned.replace("t.me/", "")
    
    cleaned = cleaned.lstrip("@").strip()
    if not re.match(r"^[a-zA-Z0-9_]{3,32}$", cleaned):
        raise HTTPException(
            status_code=400,
            detail="Iltimos to'g'ri Telegram username kiriting (masalan: @username yoki https://t.me/username)"
        )
    return f"@{cleaned}"

@router.post("/contact-requests", response_model=ContactRequestResponse)
async def create_contact_request(
    request_in: ContactRequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Honeypot anti-spam check
    if request_in.honeypot and len(request_in.honeypot.strip()) > 0:
        raise HTTPException(status_code=400, detail="Invalid submission")

    # Validate contact method
    if request_in.contact_method not in ["telegram", "whatsapp", "email"]:
        raise HTTPException(status_code=400, detail="Contact method must be telegram, whatsapp, or email.")

    contact_val = request_in.contact_value
    if request_in.contact_method == "telegram":
        contact_val = normalize_telegram_username(request_in.contact_value)

    db_req = ContactRequest(
        name=request_in.name,
        service_id=request_in.service_id,
        service_name=request_in.service_name,
        description=request_in.description,
        contact_method=request_in.contact_method,
        contact_value=contact_val,
        language=request_in.language or "uz"
    )
    db.add(db_req)
    db.commit()
    db.refresh(db_req)

    # Broadcast notification to Telegram admins
    background_tasks.add_task(send_contact_request_alert, db_req)

    return db_req
