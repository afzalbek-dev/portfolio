import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal, Base, engine
from app.models.models import AdminUser, Service, Project, ContactSetting, SiteSettings
from app.core.config import settings

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("[*] Seeding Database...")

        # 1. Seed Telegram Admin Users
        for admin_id in settings.admin_ids:
            admin_obj = db.query(AdminUser).filter(AdminUser.telegram_id == admin_id).first()
            if not admin_obj:
                db.add(AdminUser(telegram_id=admin_id, username="admin", full_name="Super Admin", is_superadmin=True))
                print(f"[+] Admin user added with Telegram ID: {admin_id}")

        # 2. Seed Services
        if db.query(Service).count() == 0:
            services_data = [
                {
                    "slug": "telegram_bot",
                    "icon": "Bot",
                    "order_index": 1,
                    "title_uz": "Telegram Bot Yaratish",
                    "title_ru": "Разработка Telegram-ботов",
                    "title_en": "Telegram Bot Development",
                    "desc_uz": "Savdo, CRM, obuna, to'lovlar va avtomatlashtirish uchun Telegram botlar.",
                    "desc_ru": "Бот для продаж, CRM, подписок, платежей и работы с клиентами.",
                    "desc_en": "High-performance Telegram bots for e-commerce, CRM, subscriptions, and automation.",
                    "price": "Negotiable / Kelishiladi",
                    "features_uz": ["Click/Payme Integratsiya", "Admin Bot Panel", "Avto-xabar yuborish"],
                    "features_ru": ["Интеграция Click/Payme", "Админ бот панель", "Рассылки"],
                    "features_en": ["Payment Gateways", "Admin Bot Panel", "Broadcast Systems"]
                },
                {
                    "slug": "website",
                    "icon": "Globe",
                    "order_index": 2,
                    "title_uz": "Veb-saytlar Yaratish",
                    "title_ru": "Разработка сайтов",
                    "title_en": "Website Development",
                    "desc_uz": "Landing page, korporativ saytlar, portfolio va murakkab veb-tizimlar.",
                    "desc_ru": "Лендинги, корпоративные сайты, портфолио и сложные веб-системы.",
                    "desc_en": "Landing pages, corporate websites, portfolio sites, and custom web portals.",
                    "price": "Negotiable / Kelishiladi",
                    "features_uz": ["SEO Optimal", "Adaptiv Dizayn", "Tezkor Yuklanish"],
                    "features_ru": ["SEO-оптимизация", "Адаптивный дизайн", "Быстрая загрузка"],
                    "features_en": ["SEO Ready", "Responsive Layout", "High Speed"]
                },
                {
                    "slug": "mini_app",
                    "icon": "Smartphone",
                    "order_index": 3,
                    "title_uz": "Telegram Mini Apps",
                    "title_ru": "Telegram Mini Apps",
                    "title_en": "Telegram Mini Apps",
                    "desc_uz": "Telegram ichida ishlovchi zamonaviy interaktiv Web App interfeyslari.",
                    "desc_ru": "Современные Web Apps внутри Telegram с возможностями сайта.",
                    "desc_en": "Rich React web apps running smoothly directly inside Telegram messenger.",
                    "price": "Negotiable / Kelishiladi",
                    "features_uz": ["React Frontend", "FastAPI Backend", "Seamless Auth"],
                    "features_ru": ["React Frontend", "FastAPI Бэкенд", "Бесшовная авторизация"],
                    "features_en": ["React UI", "FastAPI Backend", "Seamless Auth"]
                },
                {
                    "slug": "backend_api",
                    "icon": "Server",
                    "order_index": 4,
                    "title_uz": "Backend va API",
                    "title_ru": "Бэкенд и API",
                    "title_en": "Backend & API",
                    "desc_uz": "Python va FastAPI asosida xavfsiz va kengayuvchan server arxitekturasi.",
                    "desc_ru": "Мощная серверная архитектура на Python, FastAPI и PostgreSQL.",
                    "desc_en": "Scalable RESTful APIs and backend infrastructure powered by FastAPI.",
                    "price": "Negotiable / Kelishiladi",
                    "features_uz": ["FastAPI / Swagger", "JWT Security", "PostgreSQL"],
                    "features_ru": ["FastAPI / Swagger", "JWT Авторизация", "PostgreSQL"],
                    "features_en": ["FastAPI / Swagger", "JWT Security", "PostgreSQL"]
                },
                {
                    "slug": "ai_solutions",
                    "icon": "Sparkles",
                    "order_index": 5,
                    "title_uz": "AI va Sun'iy Intelekt",
                    "title_ru": "AI и ИИ Решения",
                    "title_en": "AI Solutions",
                    "desc_uz": "OpenAI, Gemini integratsiyasi va AI rasm/video generatsiyasi.",
                    "desc_ru": "Интеграция OpenAI/Gemini, генерация ИИ видео/изображений.",
                    "desc_en": "Integration of Gemini/OpenAI models, AI Image & Video generation.",
                    "price": "Negotiable / Kelishiladi",
                    "features_uz": ["Gemini / OpenAI", "AI Video & Image", "Smart Botlar"],
                    "features_ru": ["Gemini / OpenAI", "AI Видео и Фото", "Умные боты"],
                    "features_en": ["Gemini & OpenAI", "AI Video & Photo", "Smart Bots"]
                },
                {
                    "slug": "automation",
                    "icon": "Zap",
                    "order_index": 6,
                    "title_uz": "Avtomatlashtirish",
                    "title_ru": "Автоматизация",
                    "title_en": "Automation Systems",
                    "desc_uz": "Biznes jarayonlarini avtomatlashtirish va botlar orqali xabarnomalar.",
                    "desc_ru": "Автоматизация бизнес-процессов и внутренних сервисов.",
                    "desc_en": "Custom workflow automation scripts and scheduled bots.",
                    "price": "Negotiable / Kelishiladi",
                    "features_uz": ["Telegram Parse", "Cron Tasks", "Webhooks"],
                    "features_ru": ["Парсинг Telegram", "Cron Задачи", "Webhooks"],
                    "features_en": ["Telegram Scraping", "Cron Jobs", "Webhooks"]
                }
            ]
            for s in services_data:
                db.add(Service(**s))
            print("[+] Services seeded successfully.")

        # 3. Seed Projects (Empty list by default - managed via Telegram Bot)
        if db.query(Project).count() == 0:
            print("[+] Projects ready for Telegram Bot management.")

        # 4. Seed Contact Settings
        contacts_seed = [
            ("telegram_username", "@Obunachi786", True),
            ("whatsapp_number", "+998908734005", True),
            ("phone", "+998908734005", True),
            ("instagram", "@developer_username", True),
            ("email", "dev@example.com", True),
            ("github", "https://github.com", True),
            ("youtube", "https://youtube.com", False)
        ]
        for key, val, enabled in contacts_seed:
            if not db.query(ContactSetting).filter(ContactSetting.key == key).first():
                db.add(ContactSetting(key=key, value=val, is_enabled=enabled))

        # 5. Seed Site Settings
        default_settings = [
            ("site_name", "DevPortfolio", "DevPortfolio", "DevPortfolio"),
            ("hero_title", "Telegram Bot, Web va AI Developer", "Разработчик Telegram-ботов, сайтов и AI-решений", "Telegram Bot, Web & AI Developer"),
            ("hero_subtitle", "Biznes, shaxsiy loyiha va startaplar uchun zamonaviy Telegram botlar, saytlar va AI yechimlar yarataman.", "Разрабатываю современные Telegram-боты, сайты и AI-решения для бизнеса, стартапов и личных проектов.", "I build modern Telegram bots, websites and AI-powered solutions for businesses, startups and personal projects."),
            ("about_text", "Men Python, FastAPI, Aiogram va React texnologiyalariga ixtisoslashgan dasturchiman. 4 yildan ortiq tajribaga egaman.", "Я разработчик, специализирующийся на Python, FastAPI, Aiogram и React. Более 4 лет опыта.", "Full-stack software engineer specialized in Python, FastAPI, Aiogram & React with over 4 years of experience."),
            ("developer_name", "Developer Name", "Имя Разработчика", "Developer Name"),
            ("developer_title", "Telegram & Web AI Solutions", "Telegram & Web AI Solutions", "Telegram & Web AI Solutions"),
            ("seo_title", "Developer Portfolio | Telegram Bot, Web & AI", "Developer Portfolio | Telegram Bot, Web & AI", "Developer Portfolio | Telegram Bot, Web & AI"),
            ("seo_desc", "Custom Telegram bots, web apps, and AI solutions", "Custom Telegram bots, web apps, and AI solutions", "Custom Telegram bots, web apps, and AI solutions"),
            ("contact_form_enabled", "true", "true", "true"),
            ("maintenance_mode", "false", "false", "false")
        ]

        for key, uz, ru, en in default_settings:
            if not db.query(SiteSettings).filter(SiteSettings.key == key).first():
                db.add(SiteSettings(key=key, val_uz=uz, val_ru=ru, val_en=en))

        db.commit()
        print("[+] Database seeding completed cleanly!")
    except Exception as e:
        db.rollback()
        print(f"[-] Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
