import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.db import is_authorized_admin
from bot.keyboards.keyboards import get_main_admin_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    
    if not is_authorized_admin(message.from_user.id):
        await message.answer(
            "👋 **Assalomu alaykum!**\n\nBu portfolio va raqamli loyihalar rasmiy boti. Veb-saytimiz orqali xizmat buyurtma qilishingiz mumkin.",
            parse_mode="Markdown"
        )
        return

    await message.answer(
        f"👋 **Xush kelibsiz, Admin!**\n\nBu bot orqali veb-saytning barcha kontenti, portfolio, xizmatlar va kelgan buyurtmalarni to'liq boshqarishingiz mumkin.",
        reply_markup=get_main_admin_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "fsm_cancel")
async def cancel_fsm(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("❌ Jarayon bekor qilindi.")
    await callback.message.edit_text("❌ Jarayon bekor qilindi va asosiy menyuga qaytildi.")

@router.message(F.text == "🔄 Refresh Data")
async def refresh_data(message: Message, state: FSMContext):
    if not is_authorized_admin(message.from_user.id): return
    await state.clear()
    await message.answer("✅ Barcha ma'lumotlar va sessiyalar yangilandi.", reply_markup=get_main_admin_keyboard())
