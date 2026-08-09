from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database.session import get_db
from app.models.models import SiteSettings, ContactSetting

router = APIRouter(tags=["Settings"])

@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    settings_list = db.query(SiteSettings).all()
    contacts_list = db.query(ContactSetting).filter(ContactSetting.is_enabled == True).all()

    result: Dict[str, Any] = {
        "site_settings": {},
        "contacts": {}
    }

    for s in settings_list:
        result["site_settings"][s.key] = {
            "uz": s.val_uz or "",
            "ru": s.val_ru or "",
            "en": s.val_en or ""
        }

    for c in contacts_list:
        result["contacts"][c.key] = c.value

    # Extract Telegram username to generate personal direct link
    tg_user = result["contacts"].get("telegram_username") or "@developer_username"
    clean_username = tg_user.replace("@", "").strip()
    result["admin_telegram_link"] = f"https://t.me/{clean_username}"

    return result

@router.get("/about")
def get_about(db: Session = Depends(get_db)):
    settings_list = db.query(SiteSettings).all()
    about_data = {}
    for s in settings_list:
        if s.key in ["developer_name", "developer_title", "about_text", "hero_title", "hero_subtitle"]:
            about_data[s.key] = {
                "uz": s.val_uz or "",
                "ru": s.val_ru or "",
                "en": s.val_en or ""
            }
    return about_data

@router.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    contacts_list = db.query(ContactSetting).filter(ContactSetting.is_enabled == True).all()
    res = {}
    for c in contacts_list:
        res[c.key] = c.value
    
    tg_user = res.get("telegram_username", "@developer_username")
    clean = tg_user.replace("@", "").strip()
    res["admin_telegram_link"] = f"https://t.me/{clean}"
    return res
