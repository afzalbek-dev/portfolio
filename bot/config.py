import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../backend/portfolio.db")

# Parse Admin IDs from env
raw_admin_id = os.getenv("TELEGRAM_ADMIN_ID", "")
raw_admin_ids = os.getenv("TELEGRAM_ADMIN_IDS", "")

DEFAULT_ADMIN_IDS = set()
for item in (raw_admin_ids + "," + raw_admin_id).split(","):
    cleaned = item.strip()
    if cleaned.isdigit():
        DEFAULT_ADMIN_IDS.add(int(cleaned))

# Server upload directory for storing uploaded Telegram images & videos
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
