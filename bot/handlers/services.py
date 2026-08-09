import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.db import get_db, is_authorized_admin, Service
from bot.states.states import ServiceFSM
from bot.keyboards.keyboards import get_service_menu_keyboard, get_cancel_skip_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🛠 Services")
async def services_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    await message.answer(
        "🛠 **XIZMATLAR BO'LIMI**\n\nVeb-saytdagi xizmatlar va narxlarni boshqarish:",
        reply_markup=get_service_menu_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "serv_list")
async def list_services(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    db = get_db()
    try:
        services = db.query(Service).order_by(Service.order_index).all()
        if not services:
            await callback.answer("📭 Xizmatlar topilmadi.", show_alert=True)
            return

        await callback.answer()
        await callback.message.answer(f"🛠 **Jami {len(services)} ta xizmat mavjud:**", parse_mode="Markdown")

        for s in services:
            status = "✅ Faol" if s.is_active else "❌ Faol emas"
            text = f"""🛠 **{s.title_uz}**
📌 **Slug**: `{s.slug}`
📝 **Tavsif**: {s.desc_uz}
💰 **Boshlang'ich narx**: {s.price}
📌 **Holat**: {status}
"""
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="👁 Yoqish/O'chirish", callback_data=f"toggle_serv_{s.id}"),
                InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"del_serv_{s.id}")
            ]])
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    finally:
        db.close()

# ----------------- ADD SERVICE FSM -----------------

@router.callback_query(F.data == "serv_add")
async def start_add_service(callback: CallbackQuery, state: FSMContext):
    if not is_authorized_admin(callback.from_user.id): return
    await state.set_state(ServiceFSM.title_uz)
    await callback.message.answer("1️⃣ Xizmat nomini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ServiceFSM.title_uz)
async def process_serv_title_uz(message: Message, state: FSMContext):
    await state.update_data(title_uz=message.text)
    await state.set_state(ServiceFSM.title_ru)
    await message.answer("2️⃣ Xizmat nomini **Ruscha (RU)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ServiceFSM.title_ru)
async def process_serv_title_ru(message: Message, state: FSMContext):
    await state.update_data(title_ru=message.text)
    await state.set_state(ServiceFSM.title_en)
    await message.answer("3️⃣ Xizmat nomini **Inglizcha (EN)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ServiceFSM.title_en)
async def process_serv_title_en(message: Message, state: FSMContext):
    await state.update_data(title_en=message.text)
    await state.set_state(ServiceFSM.desc_uz)
    await message.answer("4️⃣ Xizmat tavsifini **O'zbekcha (UZ)** kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ServiceFSM.desc_uz)
async def process_serv_desc_uz(message: Message, state: FSMContext):
    await state.update_data(desc_uz=message.text, desc_ru=message.text, desc_en=message.text)
    await state.set_state(ServiceFSM.price)
    await message.answer("5️⃣ Boshlang'ich narxi yoki 'Kelishiladi' deb kiriting:", reply_markup=get_cancel_skip_keyboard(False))

@router.message(ServiceFSM.price)
async def process_serv_price(message: Message, state: FSMContext):
    data = await state.get_data()
    slug_gen = data.get("title_uz").lower().replace(" ", "_")[:20]

    db = get_db()
    try:
        new_s = Service(
            slug=slug_gen,
            icon="Bot",
            title_uz=data.get("title_uz"),
            title_ru=data.get("title_ru"),
            title_en=data.get("title_en"),
            desc_uz=data.get("desc_uz"),
            desc_ru=data.get("desc_ru"),
            desc_en=data.get("desc_en"),
            price=message.text,
            is_active=True
        )
        db.add(new_s)
        db.commit()

        await state.clear()
        await message.answer(f"🎉 **Xizmat '{new_s.title_uz}' muvaffaqiyatli qo'shildi!**", parse_mode="Markdown")
    finally:
        db.close()

# ----------------- TOGGLE & DELETE -----------------

@router.callback_query(F.data.startswith("toggle_serv_"))
async def toggle_service_status(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    sid = int(callback.data.split("_")[2])
    db = get_db()
    try:
        s = db.query(Service).filter(Service.id == sid).first()
        if s:
            s.is_active = not s.is_active
            db.commit()
            status = "✅ Yoqildi" if s.is_active else "❌ O'chirildi"
            await callback.answer(f"Xizmat holati: {status}", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data.startswith("del_serv_"))
async def delete_service(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    sid = int(callback.data.split("_")[2])
    db = get_db()
    try:
        s = db.query(Service).filter(Service.id == sid).first()
        if s:
            db.delete(s)
            db.commit()
            await callback.answer("🗑 Xizmat o'chirildi!", show_alert=True)
            await callback.message.edit_text("🗑 **Xizmat ro'yxatdan o'chirildi.**", parse_mode="Markdown")
    finally:
        db.close()
