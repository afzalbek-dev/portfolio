from datetime import datetime, timezone
from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, DateTime, JSON
from app.database.session import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(100), nullable=True)
    full_name = Column(String(150), nullable=True)
    is_superadmin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    icon = Column(String(50), default="Bot")
    
    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=False)
    desc_ru = Column(Text, nullable=False)
    desc_en = Column(Text, nullable=False)

    features_uz = Column(JSON, default=list)
    features_ru = Column(JSON, default=list)
    features_en = Column(JSON, default=list)

    price = Column(String(100), default="Negotiable / Kelishiladi")
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    title_uz = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)

    desc_uz = Column(Text, nullable=False)
    desc_ru = Column(Text, nullable=False)
    desc_en = Column(Text, nullable=False)

    category = Column(String(50), index=True, nullable=False)
    cover_image = Column(Text, nullable=True)
    screenshots = Column(JSON, default=list)
    video_url = Column(Text, nullable=True)

    demo_url = Column(Text, nullable=True)
    bot_url = Column(Text, nullable=True)
    website_url = Column(Text, nullable=True)
    github_url = Column(Text, nullable=True)

    tech_stack = Column(JSON, default=list)
    is_published = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ContactSetting(Base):
    __tablename__ = "contact_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False) # telegram_username, whatsapp_number, phone, instagram, email, github, youtube
    value = Column(String(255), nullable=True)
    is_enabled = Column(Boolean, default=True)

class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    service_id = Column(String(50), nullable=True)
    service_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)

    contact_method = Column(String(20), nullable=False) # telegram, whatsapp, email
    contact_value = Column(String(150), nullable=False)
    
    language = Column(String(10), default="uz")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    
    val_uz = Column(Text, nullable=True)
    val_ru = Column(Text, nullable=True)
    val_en = Column(Text, nullable=True)
