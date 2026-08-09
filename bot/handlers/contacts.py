import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, ContactSetting
from bot.states.states import ContactFSM
from bot.keyboards.keyboards import get_cancel_skip_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📞 Contacts")
async def contacts_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    
    db = get_db()
    try:
        contacts = db.query(ContactSetting).all()
        buttons = []

        text = "📞 **BOG'LANISH VA ALOQA KANALLARI**\n\nHar bir aloqa kanalini tahrirlashingiz yoki yoqib/o'chirishingiz mumkin:\n\n"
        
        for c in contacts:
            status = "✅ Faol" if c.is_enabled else "❌ O'chirilgan"
            text += f"• **{c.key.upper()}**: `{c.value}` ({status})\n"
            
            btn_text = "❌ O'chirish" if c.is_enabled else "✅ Yoqish"
            buttons.append([
                InlineKeyboardButton(text=f"✏️ {c.key.upper()}", callback_data=f"edit_cnt_{c.key}"),
                InlineKeyboardButton(text=btn_text, callback_data=f"tog_cnt_{c.key}")
            ])

        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data.startswith("tog_cnt_"))
async def toggle_contact(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    key = callback.data.split("_")[2]
    db = get_db()
    try:
        c = db.query(ContactSetting).filter(ContactSetting.key == key).first()
        if c:
            c.is_enabled = not c.is_enabled
            db.commit()
            st = "✅ Yoqildi" if c.is_enabled else "❌ O'chirildi"
            await callback.answer(f"{key.upper()} {st}!", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data.startswith("edit_cnt_"))
async def start_edit_contact(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    key = callback.data.split("_")[2]
    await state.update_data(contact_key=key)
    await state.set_state(ContactFSM.edit_value)
    await callback.message.answer(f"✏️ **{key.upper()}** uchun yangi qiymatni kiriting:", reply_markup=get_cancel_skip_keyboard(False), parse_mode="Markdown")

@router.message(ContactFSM.edit_value)
async def process_new_contact_value(message: Message, state: FSMContext):
    data = await state.get_data()
    key = data.get("contact_key")
    db = get_db()
    try:
        c = db.query(ContactSetting).filter(ContactSetting.key == key).first()
        if not c:
            c = ContactSetting(key=key)
            db.add(c)
        c.value = message.text
        c.is_enabled = True
        db.commit()

        await state.clear()
        await message.answer(f"✅ **{key.upper()}** muvaffaqiyatli yangilandi: `{message.text}`", parse_mode="Markdown")
    finally:
        db.close()
