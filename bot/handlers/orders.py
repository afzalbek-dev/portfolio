import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.db import get_db, is_authorized_admin, Order
from bot.keyboards.keyboards import get_orders_filter_keyboard, get_order_detail_keyboard, get_main_admin_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "📩 Orders")
async def orders_menu(message: Message):
    if not is_authorized_admin(message.from_user.id): return
    await message.answer(
        "📦 **BUYURTMALAR BO'LIMI**\n\nQaysi holatdagi buyurtmalarni ko'rmoqchisiz?",
        reply_markup=get_orders_filter_keyboard(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("ordfilter_"))
async def list_filtered_orders(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    
    status_filter = callback.data.split("_")[1]
    db = get_db()
    try:
        query = db.query(Order)
        if status_filter != "all":
            query = query.filter(Order.status == status_filter)
        
        orders = query.order_by(Order.created_at.desc()).all()
        
        if not orders:
            await callback.answer("📭 Ushbu bo'limda buyurtmalar topilmadi.", show_alert=True)
            return

        await callback.answer()
        await callback.message.answer(f"📊 **Jami {len(orders)} ta buyurtma topildi:**", parse_mode="Markdown")

        for o in orders[:5]:  # Display top 5 latest
            status_icon = {
                "new": "🆕 Yangi",
                "accepted": "✅ Qabul qilingan",
                "in_progress": "⏳ Jarayonda",
                "completed": "✔️ Bajarilgan",
                "cancelled": "❌ Bekor qilingan"
            }.get(o.status, o.status)

            lang_flag = {"uz": "🇺🇿 Uzbek", "ru": "🇷🇺 Russian", "en": "🇬🇧 English"}.get(o.language, o.language)

            text = f"""📦 **BUYURTMA #{o.id}**

👤 **Mijoz**: {o.name}
🛠 **Xizmat**: {o.service_name or o.service_id or 'Umumiy'}
📝 **Tavsif**:
{o.description}

💰 **Budjet**: {o.budget or "Ko'rsatilmadi"}
🌍 **Til**: {lang_flag}
📌 **Holat**: {status_icon}
🕒 **Sana**: {o.created_at.strftime("%d.%m.%Y %H:%M")}
"""
            kb = get_order_detail_keyboard(
                order_id=o.id,
                phone=o.phone,
                telegram=o.telegram,
                whatsapp=o.whatsapp,
                instagram=o.instagram
            )
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

    finally:
        db.close()

@router.callback_query(F.data.startswith("status_"))
async def update_order_status_callback(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    
    parts = callback.data.split("_")
    order_id = int(parts[1])
    new_status = "_".join(parts[2:])

    db = get_db()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            await callback.answer("❌ Buyurtma topilmadi", show_alert=True)
            return

        order.status = new_status
        db.commit()

        status_text = {
            "accepted": "✅ Qabul qilindi",
            "in_progress": "⏳ Jarayonga o'tkazildi",
            "completed": "✔️ Bajarildi deb belgilandi",
            "cancelled": "❌ Bekor qilindi"
        }.get(new_status, new_status)

        await callback.answer(f"Buyurtma #{order_id} {status_text}!", show_alert=True)
        await callback.message.edit_text(callback.message.text + f"\n\n👉 **Yangi holat**: {status_text}", parse_mode="Markdown")
    finally:
        db.close()

@router.callback_query(F.data.startswith("confirm_del_ord_"))
async def confirm_delete_order(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    order_id = int(callback.data.split("_")[3])
    
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⚠️ Ha, o'chirilsin", callback_data=f"del_ord_{order_id}"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ordfilter_all")
    ]])
    await callback.message.reply(f"❓ **Rostdan ham #{order_id} sonli buyurtmani o'chirmoqchimisiz?**", reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data.startswith("del_ord_"))
async def delete_order_callback(callback: CallbackQuery):
    if not is_authorized_admin(callback.from_user.id): return
    order_id = int(callback.data.split("_")[2])

    db = get_db()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            db.delete(order)
            db.commit()
            await callback.answer("🗑 Buyurtma o'chirildi!", show_alert=True)
            await callback.message.edit_text(f"🗑 **Buyurtma #{order_id} o'chirildi.**", parse_mode="Markdown")
    finally:
        db.close()
