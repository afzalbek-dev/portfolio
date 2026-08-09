import logging
from aiogram import Router, F
from aiogram.types import Message
from bot.db import get_db, is_authorized_admin, Order, Project, VideoProject, Service

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📊 Statistics")
async def show_stats(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    
    db = get_db()
    try:
        total_orders = db.query(Order).count()
        new_cnt = db.query(Order).filter(Order.status == "new").count()
        acc_cnt = db.query(Order).filter(Order.status == "accepted").count()
        prog_cnt = db.query(Order).filter(Order.status == "in_progress").count()
        comp_cnt = db.query(Order).filter(Order.status == "completed").count()
        canc_cnt = db.query(Order).filter(Order.status == "cancelled").count()

        total_projects = db.query(Project).count()
        pub_projects = db.query(Project).filter(Project.is_published == True).count()

        total_videos = db.query(VideoProject).count()
        total_services = db.query(Service).count()

        text = f"""📊 **VEB-SAYT VA TIZIM STATISTIKASI**

📦 **BUYURTMALAR**:
• Jami: **{total_orders}**
• 🆕 Yangi: **{new_cnt}**
• ✅ Qabul qilingan: **{acc_cnt}**
• ⏳ Jarayonda: **{prog_cnt}**
• ✔️ Bajarilgan: **{comp_cnt}**
• ❌ Bekor qilingan: **{canc_cnt}**

💼 **PORTFOLIO VA MEDIA**:
• Portfolio loyihalari: **{pub_projects} / {total_projects}** (Chop etilgan)
• Video roliklar: **{total_videos}**
• Xizmatlar turlari: **{total_services}**
"""
        await message.answer(text, parse_mode="Markdown")
    finally:
        db.close()
