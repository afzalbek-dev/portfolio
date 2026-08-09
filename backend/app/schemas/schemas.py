from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ServiceResponse(BaseModel):
    id: int
    slug: str
    icon: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str
    desc_ru: str
    desc_en: str
    features_uz: Optional[List[str]] = []
    features_ru: Optional[List[str]] = []
    features_en: Optional[List[str]] = []
    price: Optional[str] = "Negotiable / Kelishiladi"
    order_index: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: int
    category: str
    title_uz: str
    title_ru: str
    title_en: str
    desc_uz: str
    desc_ru: str
    desc_en: str
    cover_image: Optional[str] = None
    screenshots: Optional[List[str]] = []
    video_url: Optional[str] = None
    demo_url: Optional[str] = None
    bot_url: Optional[str] = None
    website_url: Optional[str] = None
    github_url: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    is_published: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class ContactRequestCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    description: str = Field(..., min_length=3)
    contact_method: str = Field(..., description="whatsapp, telegram, or email")
    contact_value: str = Field(..., min_length=2, max_length=150)
    language: Optional[str] = "uz"
    honeypot: Optional[str] = None # Anti-spam

class ContactRequestResponse(BaseModel):
    id: int
    name: str
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    description: str
    contact_method: str
    contact_value: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True
