import os
import uuid
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, Project
from bot.states.states import ProjectFSM
from bot.config import UPLOAD_DIR
from bot.keyboards.keyboards import get_portfolio_menu_keyboard, get_cancel_skip_keyboard, get_category_picker_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "💼 Portfolio")
async def portfolio_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    await message.answer(
        "💼 **PORTFOLIO VA LOYIHALAR BO'LIMI**\n\nVeb-saytdagi loyihalarni boshqarish uchun kerakli amalni tanlang:",
        reply_markup=get_portfolio_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "port_list")
async def list_portfolio(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    db = get_db()
    try:
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
        if not projects:
            await callback.answer("📭 Portfolio loyihalari topilmadi.", show_alert=True)
            return

        await callback.answer()
        await callback.message.answer(f"💼 **Jami {len(projects)} ta loyiha mavjud:**", parse_mode="Markdown")

        for p in projects:
            pub_status = "👁 Chop etilgan" if p.is_published else "🙈 Yashirilgan"
            text = f"""📌 **{p.title_uz}**
📂 **Kategoriya**: {p.category}
📝 **Tavsif**: {p.desc_uz[:100]}...
🛠 **Texnologiyalar**: {", ".join(p.tech_stack or [])}
📌 **Holat**: {pub_status}
"""
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="👁 Chop etish/Yashirish", callback_data=f"toggle_pub_p_{p.id}"),
                InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_proj_{p.id}")
            ]])
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    finally:
        db.close()

# ----------------- ADD PROJECT FSM WIZARD -----------------

@router.callback_query(F.data == "port_add")
async def start_add_project(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    await state.set_state(ProjectFSM.category)
    await callback.message.answer("1️⃣ Loyiha kategoriyasini tanlang:", reply_markup=get_category_picker_keyboard())

@router.callback_query(ProjectFSM.category, F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    cat_name = callback.data.replace("cat_", "")
    await state.update_data(category=cat_name)
    await state.set_state(ProjectFSM.title_uz)
    await callback.message.answer("2️⃣ Loyiha nomini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ProjectFSM.title_uz)
async def process_title_uz(message: Message, state: FSMContext):
    await state.update_data(title_uz=message.text)
    await state.set_state(ProjectFSM.title_ru)
    await message.answer("3️⃣ Loyiha nomini **Ruscha (RU)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ProjectFSM.title_ru)
async def process_title_ru(message: Message, state: FSMContext):
    await state.update_data(title_ru=message.text)
    await state.set_state(ProjectFSM.title_en)
    await message.answer("4️⃣ Loyiha nomini **Inglizcha (EN)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ProjectFSM.title_en)
async def process_title_en(message: Message, state: FSMContext):
    await state.update_data(title_en=message.text)
    await state.set_state(ProjectFSM.desc_uz)
    await message.answer("5️⃣ Loyiha tavsifini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ProjectFSM.desc_uz)
async def process_desc_uz(message: Message, state: FSMContext):
    await state.update_data(desc_uz=message.text)
    await state.set_state(ProjectFSM.desc_ru)
    await message.answer("6️⃣ Loyiha tavsifini **Ruscha (RU)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ProjectFSM.desc_ru)
async def process_desc_ru(message: Message, state: FSMContext):
    await state.update_data(desc_ru=message.text)
    await state.set_state(ProjectFSM.desc_en)
    await message.answer("7️⃣ Loyiha tavsifini **Inglizcha (EN)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ProjectFSM.desc_en)
async def process_desc_en(message: Message, state: FSMContext):
    await state.update_data(desc_en=message.text)
    await state.set_state(ProjectFSM.tech_stack)
    await message.answer("8️⃣ Texnologiyalar ro'yxatini vergul bilan kiriting (masalan: Python, FastAPI, React):", reply_markup=get_cancel_skip_keyboard(True))

@router.callback_query(ProjectFSM.tech_stack, F.data == "fsm_skip")
@router.message(ProjectFSM.tech_stack)
async def process_tech_stack(event, state: FSMContext):
    val = event.text if isinstance(event, Message) else "Python, FastAPI"
    stack = [t.strip() for t in val.split(",") if t.strip()]
    await state.update_data(tech_stack=stack)
    await state.set_state(ProjectFSM.cover_image)
    
    msg = event if isinstance(event, Message) else event.message
    await msg.answer("9️⃣ Loyiha uchun muqova **Rasm (Photo)** yuboring yoki URL/Skip bosing:", reply_markup=get_cancel_skip_keyboard(True))

@router.message(ProjectFSM.cover_image, F.photo)
async def process_cover_photo(message: Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    filename = f"cover_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    await bot.download(photo, destination=filepath)
    cover_url = f"/uploads/{filename}"
    
    await state.update_data(cover_image=cover_url)
    await state.set_state(ProjectFSM.demo_url)
    await message.answer("🔟 Demo URL (Veb-sayt havolasi) kiriting yoki Skip bosing:", reply_markup=get_cancel_skip_keyboard(True))

@router.callback_query(ProjectFSM.cover_image, F.data == "fsm_skip")
@router.message(ProjectFSM.cover_image)
async def process_cover_text(event, state: FSMContext):
    cover_url = event.text if isinstance(event, Message) else "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&q=80"
    await state.update_data(cover_image=cover_url)
    await state.set_state(ProjectFSM.demo_url)
    msg = event if isinstance(event, Message) else event.message
    await msg.answer("🔟 Demo URL kiriting yoki Skip bosing:", reply_markup=get_cancel_skip_keyboard(True))

@router.callback_query(ProjectFSM.demo_url, F.data == "fsm_skip")
@router.message(ProjectFSM.demo_url)
async def process_demo_url(event, state: FSMContext):
    val = event.text if isinstance(event, Message) else None
    await state.update_data(demo_url=val)
    await state.set_state(ProjectFSM.bot_url)
    msg = event if isinstance(event, Message) else event.message
    await msg.answer("1️⃣1️⃣ Telegram Bot URL (t.me/...) kiriting yoki Skip bosing:", reply_markup=get_cancel_skip_keyboard(True))

@router.callback_query(ProjectFSM.bot_url, F.data == "fsm_skip")
@router.message(ProjectFSM.bot_url)
async def process_bot_url(event, state: FSMContext):
    val = event.text if isinstance(event, Message) else None
    await state.update_data(bot_url=val)
    await state.set_state(ProjectFSM.github_url)
    msg = event if isinstance(event, Message) else event.message
    await msg.answer("1️⃣2️⃣ GitHub Repository URL kiriting yoki Skip bosing:", reply_markup=get_cancel_skip_keyboard(True))

@router.callback_query(ProjectFSM.github_url, F.data == "fsm_skip")
@router.message(ProjectFSM.github_url)
async def process_github_url(event, state: FSMContext):
    val = event.text if isinstance(event, Message) else None
    data = await state.get_data()
    
    # Save project to database
    db = get_db()
    try:
        new_project = Project(
            category=data.get("category", "bot"),
            title_uz=data.get("title_uz", "Loyiha"),
            title_ru=data.get("title_ru", "Проект"),
            title_en=data.get("title_en", "Project"),
            desc_uz=data.get("desc_uz", ""),
            desc_ru=data.get("desc_ru", ""),
            desc_en=data.get("desc_en", ""),
            tech_stack=data.get("tech_stack", ["Python"]),
            cover_image=data.get("cover_image"),
            demo_url=data.get("demo_url"),
            bot_url=data.get("bot_url"),
            github_url=val,
            is_published=True
        )
        db.add(new_project)
        db.commit()
        
        await state.clear()
        msg = event if isinstance(event, Message) else event.message
        await msg.answer(f"🎉 **Loyiha '{new_project.title_uz}' muvaffaqiyatli saqlandi va saytga joylandi!**", parse_mode="Markdown")
    finally:
        db.close()

# ----------------- TOGGLE & DELETE ACTIONS -----------------

@router.callback_query(F.data.startswith("toggle_pub_p_"))
async def toggle_publish_project(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    pid = int(callback.data.split("_")[3])
    db = get_db()
    try:
        proj = db.query(Project).filter(Project.id == pid).first()
        if proj:
            proj.is_published = not proj.is_published
            db.commit()
            status = "👁 Chop etildi" if proj.is_published else "🙈 Yashirildi"
            await callback.answer(f"Loyiha holati: {status}", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data.startswith("del_proj_"))
async def delete_project(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    pid = int(callback.data.split("_")[2])
    db = get_db()
    try:
        proj = db.query(Project).filter(Project.id == pid).first()
        if proj:
            db.delete(proj)
            db.commit()
            await callback.answer("🗑 Loyiha o'chirildi!", show_alert=True)
            await callback.message.edit_text("🗑 **Loyiha portfoliodan o'chirildi.**", parse_mode="Markdown")
    finally:
        db.close()
