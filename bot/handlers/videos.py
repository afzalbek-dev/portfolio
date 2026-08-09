import os
import uuid
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, VideoProject
from bot.states.states import VideoFSM
from bot.config import UPLOAD_DIR
from bot.keyboards.keyboards import get_video_menu_keyboard, get_cancel_skip_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🎬 Videos")
async def video_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    await message.answer(
        "🎬 **VIDEO PORTFOLIO VA AI ROLIKLAR BO'LIMI**\n\nVeb-saytdagi video roliklarni boshqarish:",
        reply_markup=get_video_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "vid_list")
async def list_videos(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    db = get_db()
    try:
        videos = db.query(VideoProject).order_by(VideoProject.created_at.desc()).all()
        if not videos:
            await callback.answer("📭 Video roliklar topilmadi.", show_alert=True)
            return

        await callback.answer()
        await callback.message.answer(f"🎬 **Jami {len(videos)} ta video rolik mavjud:**", parse_mode="Markdown")

        for v in videos:
            format_type = "📱 Vertikal (9:16)" if v.is_vertical else "🖥 Gorizontal (16:9)"
            pub_status = "👁 Chop etilgan" if v.is_published else "🙈 Yashirilgan"
            text = f"""🎬 **{v.title_uz}**
📝 **Tavsif**: {v.desc_uz}
📐 **Format**: {format_type}
🛠 **Instrumentlar**: {", ".join(v.tools or [])}
📌 **Holat**: {pub_status}
"""
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="👁 Chop etish/Yashirish", callback_data=f"toggle_pub_v_{v.id}"),
                InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_vid_{v.id}")
            ]])
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    finally:
        db.close()

# ----------------- ADD VIDEO FSM -----------------

@router.callback_query(F.data == "vid_add")
async def start_add_video(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    await state.set_state(VideoFSM.title_uz)
    await callback.message.answer("1️⃣ Video sarlavhasini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(VideoFSM.title_uz)
async def process_vid_title_uz(message: Message, state: FSMContext):
    await state.update_data(title_uz=message.text)
    await state.set_state(VideoFSM.title_ru)
    await message.answer("2️⃣ Video sarlavhasini **Ruscha (RU)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(VideoFSM.title_ru)
async def process_vid_title_ru(message: Message, state: FSMContext):
    await state.update_data(title_ru=message.text)
    await state.set_state(VideoFSM.title_en)
    await message.answer("3️⃣ Video sarlavhasini **Inglizcha (EN)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(VideoFSM.title_en)
async def process_vid_title_en(message: Message, state: FSMContext):
    await state.update_data(title_en=message.text)
    await state.set_state(VideoFSM.desc_uz)
    await message.answer("4️⃣ Video tavsifini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(VideoFSM.desc_uz)
async def process_vid_desc_uz(message: Message, state: FSMContext):
    await state.update_data(desc_uz=message.text, desc_ru=message.text, desc_en=message.text)
    await state.set_state(VideoFSM.video_file)
    await message.answer("5️⃣ MP4 Video faylini yuboring yoki URL manzilini matn ko'rinishida yozing:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(VideoFSM.video_file, F.video)
async def process_vid_file(message: Message, state: FSMContext, bot: Bot):
    video = message.video
    filename = f"video_{uuid.uuid4().hex[:8]}.mp4"
    filepath = os.path.join(UPLOAD_DIR, filename)
    await bot.download(video, destination=filepath)
    video_url = f"/uploads/{filename}"
    
    await state.update_data(video_url=video_url)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📱 Vertikal (9:16)", callback_data="vfmt_vert"),
        InlineKeyboardButton(text="🖥 Gorizontal (16:9)", callback_data="vfmt_horiz")
    ]])
    await state.set_state(VideoFSM.is_vertical)
    await message.answer("6️⃣ Video formatini tanlang:", reply_markup=kb)

@router.message(VideoFSM.video_file)
async def process_vid_text_url(message: Message, state: FSMContext):
    await state.update_data(video_url=message.text)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📱 Vertikal (9:16)", callback_data="vfmt_vert"),
        InlineKeyboardButton(text="🖥 Gorizontal (16:9)", callback_data="vfmt_horiz")
    ]])
    await state.set_state(VideoFSM.is_vertical)
    await message.answer("6️⃣ Video formatini tanlang:", reply_markup=kb)

@router.callback_query(VideoFSM.is_vertical, F.data.startswith("vfmt_"))
async def process_vid_format(callback: CallbackQuery, state: FSMContext):
    is_vert = callback.data == "vfmt_vert"
    data = await state.get_data()
    
    db = get_db()
    try:
        new_vid = VideoProject(
            title_uz=data.get("title_uz"),
            title_ru=data.get("title_ru"),
            title_en=data.get("title_en"),
            desc_uz=data.get("desc_uz"),
            desc_ru=data.get("desc_ru"),
            desc_en=data.get("desc_en"),
            category="ai_video",
            video_url=data.get("video_url"),
            cover_image="https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&q=80",
            tools=["Runway Gen-2", "Midjourney", "ElevenLabs"],
            is_vertical=is_vert,
            is_published=True
        )
        db.add(new_vid)
        db.commit()
        
        await state.clear()
        await callback.message.answer(f"🎉 **Video '{new_vid.title_uz}' muvaffaqiyatli qo'shildi va saytda ko'rsatiladi!**", parse_mode="Markdown")
    finally:
        db.close()

# ----------------- TOGGLE & DELETE -----------------

@router.callback_query(F.data.startswith("toggle_pub_v_"))
async def toggle_publish_video(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    vid = int(callback.data.split("_")[3])
    db = get_db()
    try:
        v = db.query(VideoProject).filter(VideoProject.id == vid).first()
        if v:
            v.is_published = not v.is_published
            db.commit()
            status = "👁 Chop etildi" if v.is_published else "🙈 Yashirildi"
            await callback.answer(f"Video holati: {status}", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data.startswith("del_vid_"))
async def delete_video(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    vid = int(callback.data.split("_")[2])
    db = get_db()
    try:
        v = db.query(VideoProject).filter(VideoProject.id == vid).first()
        if v:
            db.delete(v)
            db.commit()
            await callback.answer("🗑 Video o'chirildi!", show_alert=True)
            await callback.message.edit_text("🗑 **Video portfolio ro'yxatidan o'chirildi.**", parse_mode="Markdown")
    finally:
        db.close()
