import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, SiteSettings
from bot.states.states import SettingFSM
from bot.keyboards.keyboards import get_cancel_skip_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "⚙️ Site Settings")
async def settings_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    
    db = get_db()
    try:
        m_mode = db.query(SiteSettings).filter(SiteSettings.key == "maintenance_mode").first()
        o_form = db.query(SiteSettings).filter(SiteSettings.key == "order_form_enabled").first()
        seo_t = db.query(SiteSettings).filter(SiteSettings.key == "seo_title").first()

        m_status = "⚠️ YONIQ" if m_mode and m_mode.val_uz == "true" else "🟢 O'CHIK (Sayt ishlamoqda)"
        o_status = "🟢 YONIQ" if not o_form or o_form.val_uz == "true" else "🔴 O'CHIRILGAN"

        text = f"""⚙️ **VEB-SAYT SOZLAMALARI**

🛠 **Texnik ta'mirlash rejimi**: {m_status}
📝 **Buyurtma berish formasi**: {o_status}
🔍 **SEO Title**: {seo_t.val_uz if seo_t else 'N/A'}
"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛠 Ta'mirlash rejimini o'zgartirish", callback_data="toggle_m_mode")],
            [InlineKeyboardButton(text="📝 Buyurtma formasini yoqish/o'chirish", callback_data="toggle_o_form")],
            [InlineKeyboardButton(text="🔍 SEO Sarlavhasini tahrirlash", callback_data="edit_seo_title")]
        ])
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data == "toggle_m_mode")
async def toggle_maintenance(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    db = get_db()
    try:
        s = db.query(SiteSettings).filter(SiteSettings.key == "maintenance_mode").first()
        if not s:
            s = SiteSettings(key="maintenance_mode")
            db.add(s)
        
        curr = s.val_uz == "true"
        s.val_uz = "false" if curr else "true"
        db.commit()

        st = "⚠️ YONIQ (Sayt yopildi)" if s.val_uz == "true" else "🟢 O'CHIK (Sayt ochiq)"
        await callback.answer(f"Texnik ta'mirlash: {st}", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data == "toggle_o_form")
async def toggle_order_form(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    db = get_db()
    try:
        s = db.query(SiteSettings).filter(SiteSettings.key == "order_form_enabled").first()
        if not s:
            s = SiteSettings(key="order_form_enabled")
            db.add(s)
        
        curr = s.val_uz == "true"
        s.val_uz = "false" if curr else "true"
        db.commit()

        st = "🟢 YONIQ" if s.val_uz == "true" else "🔴 O'CHIRILGAN"
        await callback.answer(f"Buyurtma formasi: {st}", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data == "edit_seo_title")
async def start_edit_seo(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    await state.set_state(SettingFSM.edit_value)
    await callback.message.answer("🔍 Yangi SEO Title sarlavhasini kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(SettingFSM.edit_value)
async def process_seo_title(message: Message, state: FSMContext):
    db = get_db()
    try:
        s = db.query(SiteSettings).filter(SiteSettings.key == "seo_title").first()
        if not s:
            s = SiteSettings(key="seo_title")
            db.add(s)
        s.val_uz = message.text
        s.val_ru = message.text
        s.val_en = message.text
        db.commit()

        await state.clear()
        await message.answer(f"✅ **SEO Title yangilandi**: `{message.text}`", parse_mode="Markdown")
    finally:
        db.close()
