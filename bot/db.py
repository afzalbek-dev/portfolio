import os
import sys

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import AdminUser, Service, Project, ContactSetting, ContactRequest, SiteSettings
from bot.config import DATABASE_URL, DEFAULT_ADMIN_IDS

Order = ContactRequest
VideoProject = Project

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    return SessionLocal()

def is_authorized_admin(telegram_id: int) -> bool:
    if telegram_id in DEFAULT_ADMIN_IDS:
        return True
    db = get_db()
    try:
        admin = db.query(AdminUser).filter(AdminUser.telegram_id == telegram_id).first()
        return admin is not None
    finally:
        db.close()

def is_superadmin(telegram_id: int) -> bool:
    if telegram_id in DEFAULT_ADMIN_IDS:
        return True
    db = get_db()
    try:
        admin = db.query(AdminUser).filter(AdminUser.telegram_id == telegram_id).first()
        return admin.is_superadmin if admin else False
    finally:
        db.close()
