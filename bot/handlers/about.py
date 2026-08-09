import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, SiteSettings
from bot.states.states import AboutFSM
from bot.keyboards.keyboards import get_cancel_skip_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "👤 About Me")
async def about_me_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    
    db = get_db()
    try:
        hero_title = db.query(SiteSettings).filter(SiteSettings.key == "hero_title").first()
        about_text = db.query(SiteSettings).filter(SiteSettings.key == "about_text").first()

        ht_uz = hero_title.val_uz if hero_title else "N/A"
        ab_uz = about_text.val_uz if about_text else "N/A"

        text = f"""👤 **MEN HAQIMDA VA HERO BO'LIMI**

📌 **Hero Title (UZ)**: {ht_uz}
📝 **About Text (UZ)**: {ab_uz[:150]}...

Qaysi qismni tahrirlamoqchisiz?
"""
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Hero Sarlavhasini tahrirlash", callback_data="about_edit_hero")],
            [InlineKeyboardButton(text="✏️ Men haqimda matnini tahrirlash", callback_data="about_edit_text")]
        ])
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data == "about_edit_hero")
async def start_edit_hero(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    await state.set_state(AboutFSM.hero_title_uz)
    await callback.message.answer("1️⃣ Yangi Hero Sarlavhasini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(AboutFSM.hero_title_uz)
async def process_hero_uz(message: Message, state: FSMContext):
    await state.update_data(hero_title_uz=message.text)
    await state.set_state(AboutFSM.hero_title_ru)
    await message.answer("2️⃣ Yangi Hero Sarlavhasini **Ruscha (RU)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(AboutFSM.hero_title_ru)
async def process_hero_ru(message: Message, state: FSMContext):
    await state.update_data(hero_title_ru=message.text)
    await state.set_state(AboutFSM.hero_title_en)
    await message.answer("3️⃣ Yangi Hero Sarlavhasini **Inglizcha (EN)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(AboutFSM.hero_title_en)
async def process_hero_en(message: Message, state: FSMContext):
    data = await state.get_data()
    db = get_db()
    try:
        setting = db.query(SiteSettings).filter(SiteSettings.key == "hero_title").first()
        if not setting:
            setting = SiteSettings(key="hero_title")
            db.add(setting)
        
        setting.val_uz = data.get("hero_title_uz")
        setting.val_ru = data.get("hero_title_ru")
        setting.val_en = message.text
        db.commit()

        await state.clear()
        await message.answer("✅ **Hero Sarlavhasi 3 tilda muvaffaqiyatli yangilandi!**", parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data == "about_edit_text")
async def start_edit_about(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    await state.set_state(AboutFSM.about_uz)
    await callback.message.answer("1️⃣ 'Men haqimda' matnini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(AboutFSM.about_uz)
async def process_about_uz(message: Message, state: FSMContext):
    await state.update_data(about_uz=message.text)
    await state.set_state(AboutFSM.about_ru)
    await message.answer("2️⃣ 'Men haqimda' matnini **Ruscha (RU)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(AboutFSM.about_ru)
async def process_about_ru(message: Message, state: FSMContext):
    await state.update_data(about_ru=message.text)
    await state.set_state(AboutFSM.about_en)
    await message.answer("3️⃣ 'Men haqimda' matnini **Inglizcha (EN)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(AboutFSM.about_en)
async def process_about_en(message: Message, state: FSMContext):
    data = await state.get_data()
    db = get_db()
    try:
        setting = db.query(SiteSettings).filter(SiteSettings.key == "about_text").first()
        if not setting:
            setting = SiteSettings(key="about_text")
            db.add(setting)
        
        setting.val_uz = data.get("about_uz")
        setting.val_ru = data.get("about_ru")
        setting.val_en = message.text
        db.commit()

        await state.clear()
        await message.answer("✅ **'Men haqimda' matni 3 tilda muvaffaqiyatli yangilandi!**", parse_mode="Markdown")
    finally:
        db.close()
