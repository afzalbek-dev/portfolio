import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, is_superadmin, AdminUser
from bot.states.states import AdminFSM
from bot.keyboards.keyboards import get_cancel_skip_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "👥 Admins")
async def admins_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    
    db = get_db()
    try:
        admins = db.query(AdminUser).all()
        text = "👥 **TIZIM ADMINLARI RO'YXATI**\n\n"
        
        buttons = []
        for a in admins:
            role = "👑 Superadmin" if a.is_superadmin else "👤 Admin"
            text += f"• `{a.telegram_id}` - {a.full_name or a.username or 'Admin'} ({role})\n"
            if is_superadmin(message.from_user.id) and not a.is_superadmin:
                buttons.append([InlineKeyboardButton(text=f"❌ O'chirish: {a.telegram_id}", callback_data=f"del_adm_{a.telegram_id}")])

        if is_superadmin(message.from_user.id):
            buttons.insert(0, [InlineKeyboardButton(text="➕ Yangi Admin qo'shish", callback_data="add_admin_start")])

        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons), parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data == "add_admin_start")
async def start_add_admin(callback: CallbackQuery, state: FSMContext):
    if not is_superadmin(callback.from_user.id):
        await callback.answer("⛔ Faqat superadmin admin qo'sha oladi!", show_alert=True)
        return
    await state.set_state(AdminFSM.add_admin_id)
    await callback.message.answer("➕ Qo'shmoqchi bo'lgan shaxsning **Telegram User ID** raqamini kiriting (masalan: `123456789`):", reply_markup=get_cancel_skip_keyboard(False), parse_mode="Markdown")

@router.message(AdminFSM.add_admin_id)
async def process_add_admin(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos faqat raqamli Telegram ID kiriting!")
        return

    target_id = int(message.text)
    db = get_db()
    try:
        existing = db.query(AdminUser).filter(AdminUser.telegram_id == target_id).first()
        if existing:
            await message.answer(f"⚠️ Ushbu ID ({target_id}) allaqachon adminlar ro'yxatida mavjud.")
            await state.clear()
            return

        new_admin = AdminUser(telegram_id=target_id, full_name="Admin", is_superadmin=False)
        db.add(new_admin)
        db.commit()

        await state.clear()
        await message.answer(f"🎉 **Telegram ID {target_id} muvaffaqiyatli admin deb qo'shildi!**", parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data.startswith("del_adm_"))
async def remove_admin(callback: CallbackQuery):
    if not is_superadmin(callback.from_user.id):
        await callback.answer("⛔ Faqat superadmin adminni o'chira oladi!", show_alert=True)
        return
    
    target_id = int(callback.data.split("_")[2])
    db = get_db()
    try:
        adm = db.query(AdminUser).filter(AdminUser.telegram_id == target_id).first()
        if adm:
            if adm.is_superadmin:
                await callback.answer("⛔ Superadminni o'chirib bo'lmaydi!", show_alert=True)
                return
            db.delete(adm)
            db.commit()
            await callback.answer("🗑 Admin o'chirildi!", show_alert=True)
            await callback.message.edit_text(f"🗑 **Admin ID {target_id} ro'yxatdan o'chirildi.**", parse_mode="Markdown")
    finally:
        db.close()
