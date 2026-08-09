import html
import logging
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import ContactRequest, AdminUser
from app.database.session import SessionLocal

logger = logging.getLogger(__name__)

async def send_contact_request_alert(req: ContactRequest):
    """
    Broadcasts new contact request alert to all registered Telegram admins.
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram Bot Token not configured. Skipping notification broadcast.")
        return False

    admin_ids = set(settings.admin_ids)
    db = SessionLocal()
    try:
        db_admins = db.query(AdminUser).all()
        for a in db_admins:
            if a.telegram_id:
                admin_ids.add(int(a.telegram_id))
    except Exception as e:
        logger.error(f"Error fetching DB admins: {e}")
    finally:
        db.close()

    if not admin_ids:
        logger.warning("No Telegram admin IDs found to receive notification.")
        return False

    lang_flag = {"uz": "🇺🇿 Uzbek", "ru": "🇷🇺 Russian", "en": "🇬🇧 English"}.get(req.language, req.language)
    method_icon = {"telegram": "✈️ Telegram", "whatsapp": "💬 WhatsApp", "email": "📧 Email"}.get(req.contact_method, req.contact_method)
    
    date_str = req.created_at.strftime("%d.%m.%Y %H:%M")
    service_display = req.service_name or req.service_id or "Umumiy so'rov"

    safe_name = html.escape(req.name or "")
    safe_service = html.escape(service_display or "")
    safe_desc = html.escape(req.description or "")
    safe_val = html.escape(req.contact_value or "")

    text = f"""📩 <b>YANGI SO'ROV / BUYURTMA #{req.id}</b>

👤 <b>Ism</b>: {safe_name}
🛠 <b>Xizmat</b>: {safe_service}
📝 <b>Tavsif</b>:
{safe_desc}

📌 <b>Bog'lanish usuli</b>: {method_icon}
📞 <b>Aloqa qiymati</b>: <code>{safe_val}</code>
🌍 <b>Til</b>: {lang_flag}
🕒 <b>Sana</b>: {date_str}
"""

    inline_keyboard = []
    if req.contact_method == "telegram":
        username = req.contact_value.replace("@", "").strip()
        inline_keyboard.append([{"text": "✈️ Telegramda yozish", "url": f"https://t.me/{username}"}])
    elif req.contact_method == "whatsapp":
        wa_clean = "".join([c for c in req.contact_value if c.isdigit()])
        inline_keyboard.append([{"text": "💬 WhatsAppda yozish", "url": f"https://wa.me/{wa_clean}"}])
    elif req.contact_method == "email":
        inline_keyboard.append([{"text": "📧 Email yozish", "url": f"mailto:{req.contact_value}"}])

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient(timeout=10.0) as client:
        for admin_id in admin_ids:
            payload = {
                "chat_id": admin_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": {"inline_keyboard": inline_keyboard} if inline_keyboard else {}
            }
            try:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    logger.info(f"Sent contact request #{req.id} alert to Telegram admin ID: {admin_id}")
                else:
                    logger.error(f"Failed to send to admin {admin_id}: {res.text}")
            except Exception as e:
                logger.error(f"Error sending contact alert to admin {admin_id}: {e}")

    return True
