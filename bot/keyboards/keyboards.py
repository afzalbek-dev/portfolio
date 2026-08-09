from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_admin_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="💼 Portfolio"), KeyboardButton(text="🛠 Services")],
        [KeyboardButton(text="👤 About Me"), KeyboardButton(text="📞 Contacts")],
        [KeyboardButton(text="⚙️ Site Settings")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_portfolio_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Yangi ish qo'shish", callback_data="port_add")],
        [InlineKeyboardButton(text="📋 Ishlarim", callback_data="port_list")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_service_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Xizmat qo'shish", callback_data="serv_add")],
        [InlineKeyboardButton(text="📋 Xizmatlarim", callback_data="serv_list")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_video_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Video qo'shish", callback_data="vid_add")],
        [InlineKeyboardButton(text="📋 Videolarim", callback_data="vid_list")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_cancel_skip_keyboard(allow_skip=True) -> InlineKeyboardMarkup:
    row = []
    if allow_skip:
        row.append(InlineKeyboardButton(text="⏭ Skip", callback_data="fsm_skip"))
    row.append(InlineKeyboardButton(text="⬅️ Back", callback_data="fsm_cancel"))
    row.append(InlineKeyboardButton(text="❌ Cancel", callback_data="fsm_cancel"))
    return InlineKeyboardMarkup(inline_keyboard=[row])

def get_category_picker_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🤖 Telegram Bot", callback_data="cat_bot"), InlineKeyboardButton(text="🌐 Website", callback_data="cat_web")],
        [InlineKeyboardButton(text="📱 Telegram Mini App", callback_data="cat_miniapp"), InlineKeyboardButton(text="⚡ Backend/API", callback_data="cat_backend_api")],
        [InlineKeyboardButton(text="🎬 AI Video", callback_data="cat_ai_video"), InlineKeyboardButton(text="🖼 AI Image", callback_data="cat_ai_image")],
        [InlineKeyboardButton(text="⚙️ Automation", callback_data="cat_automation"), InlineKeyboardButton(text="📌 Other", callback_data="cat_other")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="fsm_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_orders_filter_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📋 Barchasi", callback_data="ordfilter_all"),
            InlineKeyboardButton(text="🆕 Yangi", callback_data="ordfilter_new")
        ],
        [
            InlineKeyboardButton(text="⏳ Jarayonda", callback_data="ordfilter_in_progress"),
            InlineKeyboardButton(text="✔️ Bajarilgan", callback_data="ordfilter_completed")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_order_detail_keyboard(order_id: int, phone: str = None, telegram: str = None, whatsapp: str = None, instagram: str = None) -> InlineKeyboardMarkup:
    buttons = []
    
    # Contact action buttons if available
    contact_row = []
    if telegram:
        clean_tg = telegram.replace("@", "").strip()
        contact_row.append(InlineKeyboardButton(text="✈️ Telegram", url=f"https://t.me/{clean_tg}"))
    if whatsapp:
        clean_wa = "".join([c for c in whatsapp if c.isdigit()])
        contact_row.append(InlineKeyboardButton(text="💬 WhatsApp", url=f"https://wa.me/{clean_wa}"))
    if phone:
        contact_row.append(InlineKeyboardButton(text=f"📞 {phone}", callback_data=f"nop_{order_id}"))
    
    if contact_row:
        buttons.append(contact_row)

    # Status update buttons
    buttons.append([
        InlineKeyboardButton(text="✅ Qabul", callback_data=f"status_{order_id}_accepted"),
        InlineKeyboardButton(text="⏳ Jarayonga", callback_data=f"status_{order_id}_in_progress")
    ])
    buttons.append([
        InlineKeyboardButton(text="✔️ Bajarildi", callback_data=f"status_{order_id}_completed"),
        InlineKeyboardButton(text="❌ Bekor", callback_data=f"status_{order_id}_cancelled")
    ])
    buttons.append([
        InlineKeyboardButton(text="🗑 Buyurtmani o'chirish", callback_data=f"confirm_del_ord_{order_id}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

get_admin_main_keyboard = get_main_admin_keyboard
get_order_status_keyboard = get_order_detail_keyboard

