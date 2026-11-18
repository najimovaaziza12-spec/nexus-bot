import logging
import random
import re
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
)

# ================= CONFIGURATION =================
BOT_TOKEN = "9251047246:AAFqgmXeQ3x_8yCTRZfXPMAP_7VSI4zhdiU"
ADMIN_CHANNEL_ID = -1004325334023
PORTFOLIO_CHANNEL_URL = "https://t.me/nexusdigitalportfolio"
WEBSITE_URL = "https://najimovaaziza12-spec.github.io/NexusDigital/"
PAYMENT_LINK = "https://t.me/Auraforge3D_Studio"

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
router = Router()

# ================= TEXTS & MULTI-LANGUAGE =================
LANGUAGES = {
    "uz": {
        "welcome": "Assalomu alaykum! <b>NexusDigital</b> kompaniyasining rasmiy botiga xush kelibsiz.\n\nIltimos, o'zingizga qulay tilni tanlang:",
        "menu": "Asosiy menyu:",
        "services": "🛍 <b>Mahsulotlar & Xizmatlar:</b>\n\nBarcha xizmatlarimiz va ularning batafsil narxlari bilan rasmiy veb-saytimizda tanishib chiqishingiz mumkin. Quyidagi tugmani bosing:",
        "portfolio": "🖼 <b>Portfolio galereyasi:</b>\nBiz bajargan eng so'nggi ishlar va loyihalar bilan tanishing. Quyidagi tugma orqali kanalimizga o'ting!",
        "faq": (
            "❓ <b>Ko'p beriladigan savollar:</b>\n\n"
            "<b>1. Buyurtma qancha vaqtda tayyor bo'ladi?</b>\n"
            "— Murakkabligiga qarab 3 kundan 2 haftagacha.\n\n"
            "<b>2. To'lov qanday amalga oshiriladi?</b>\n"
            "— Loyiha boshida <b>50% oldindan to'lov (avans)</b> qilinadi, qolgan <b>50% esa ish to'liq bitib, topshirilgandan keyin</b> to'lanadi."
        ),
        "about": "ℹ️ <b>Ma'lumot / Biz haqimizda:</b>\nBiz professional darajadagi raqamli yechimlar va dasturiy ta'minotlar yaratish bilan shug'ullanamiz. Bizning jamoamiz biznesingizni avtomatlashtirishga tayyor!",
        "website": "🌐 <b>Bizning veb-saytimiz:</b>\nRasmiy veb-saytimiz orqali batafsil ma'lumot olishingiz mumkin. Quyidagi tugmani bosing:",
        "contact": "📞 <b>Biz bilan bog'lanish:</b>\n\nTelefon orqali qo'ng'iroq qilish uchun quyidagi raqamni bosing:\n📱 <a href='tel:+998990266301'>+998 (99) 026-63-01</a>\n\nTelegram menejer: <a href='https://t.me/Auraforge3D_Studio'>@Auraforge3D_Studio</a>",
        "order_name": "🚀 <b>Buyurtma berish jarayoni</b>\n\nIltimos, ism va familiyangizni kiriting (Masalan: Azizbek):",
        "order_phone": "Rahmat, {name}! Endi telefon raqamingizni yuboring (Masalan: +998990266301):",
        "select_services": "📦 <b>Kerakli xizmatlarni tanlang</b> (Bir nechta tanlashingiz mumkin):\n\nKerakli tugmalarni bosing, tanlab bo'lgach <b>✅ Tasdiqlash</b> tugmasini bosing:",
        "order_pending": (
            "✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
            "💳 <b>To'lov sharti:</b> 50% avans va 50% ish topshirilganda.\n\n"
            "Xavfsiz to'lovni amalga oshirish yoki menejerga chekni yuborish uchun quyidagi tugmani bosing:"
        ),
        "no_services_selected": "⚠️ Kamida bitta xizmatni tanlashingiz kerak!",
        "invalid_name": "❌ Ism noto'g'ri kiritildi. Iltimos, stiker yoki rasm emas, faqat matn ko'rinishida ism kiriting (masalan: Azizbek):",
        "invalid_phone": "❌ Telefon raqam noto'g'ri. Iltimos, raqamni to'g'ri formatda kiriting (masalan: +998990266301):",
        "btn_order": "🚀 Buyurtma berish",
        "btn_services": "🛍 Mahsulotlar & Xizmatlar",
        "btn_portfolio": "🖼 Portfolio galereyasi",
        "btn_faq": "❓ Ko'p beriladigan savollar",
        "btn_about": "ℹ️ Ma'lumot",
        "btn_website": "🌐 Veb-sayt",
        "btn_contact": "📞 Biz bilan bog'lanish",
        "btn_lang": "🌐 Tilni o'zgartirish / Language",
        "back": "🔙 Ortga"
    },
    "ru": {
        "welcome": "Здравствуйте! Добро пожаловать в официальный бот компании <b>NexusDigital</b>.\n\nПожалуйста, выберите язык:",
        "menu": "Главное меню:",
        "services": "🛍 <b>Продукты и Услуги:</b>\n\nВы можете ознакомиться со всеми нашими услугами и подробными ценами на нашем официальном сайте. Нажмите кнопку ниже:",
        "portfolio": "🖼 <b>Галерея портфолио:</b>\nОзнакомьтесь с нашими последними работами и проектами в нашем канале!",
        "faq": (
            "❓ <b>Часто задаваемые вопросы:</b>\n\n"
            "<b>1. Сколько времени занимает создание?</b>\n"
            "— От 3 дней до 2 недель в зависимости от сложности.\n\n"
            "<b>2. Как осуществляется оплата?</b>\n"
            "— Вносится <b>50% предоплаты (аванс)</b> перед началом работ, а остальные <b>50% оплачиваются после полной сдачи</b> проекта."
        ),
        "about": "ℹ️ <b>Информация о нас:</b>\nМы занимаемся созданием профессиональных цифровых решений и программного обеспечения.",
        "website": "🌐 <b>Наш веб-сайт:</b>\nПосетите наш официальный сайт для получения дополнительной информации:",
        "contact": "📞 <b>Контакты:</b>\n\nНажмите на номер для звонка:\n📱 <a href='tel:+998990266301'>+998 (99) 026-63-01</a>\n\nTelegram менеджер: <a href='https://t.me/Auraforge3D_Studio'>@Auraforge3D_Studio</a>",
        "order_name": "🚀 <b>Процесс заказа</b>\n\nВведите ваше имя и фамилию (Например: Азизбек):",
        "order_phone": "Спасибо, {name}! Теперь отправьте ваш номер телефона (Например: +998990266301):",
        "select_services": "📦 <b>Выберите необходимые услуги</b> (Можно выбрать несколько):\n\nНажимайте на кнопки, а затем нажмите <b>✅ Подтвердить</b>:",
        "order_pending": (
            "✅ <b>Ваш заказ принят!</b>\n\n"
            "💳 <b>Условия оплаты:</b> 50% аванс, 50% после сдачи проекта.\n\n"
            "Для проведения безопасной оплаты нажмите кнопку ниже:"
        ),
        "no_services_selected": "⚠️ Выберите хотя бы одну услугу!",
        "invalid_name": "❌ Неверное имя. Пожалуйста, введите имя текстом (например: Азизбек):",
        "invalid_phone": "❌ Неверный номер телефона. Введите в правильном формате (например: +998990266301):",
        "btn_order": "🚀 Сделать заказ",
        "btn_services": "🛍 Продукты и Услуги",
        "btn_portfolio": "🖼 Портфолио",
        "btn_faq": "❓ FAQ",
        "btn_about": "ℹ️ Информация",
        "btn_website": "🌐 Веб-сайт",
        "btn_contact": "📞 Контакты",
        "btn_lang": "🌐 Сменить язык / Language",
        "back": "🔙 Назад"
    }
}

client_counter = 0

# Omadli mijozlar uchun 3 xil bonus ro'yxati
RANDOM_BONUSES = [
    "🎁 Bonus #1: 1 oylik bepul texnik qo'llab-quvvatlash va xatoliklarni to'g'rilash",
    "🎁 Bonus #2: Ikkinchi til (Rus tili) qo'shimchasini bepul ulab berish",
    "🎁 Bonus #3: Admin uchun 'Broadcast' (barchaga xabar yuborish) funksiyasini sovg'a qilish"
]

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_services = State()

user_languages = {}
user_selected_services = {}

ALL_SERVICES = {
    "srv_bot": "🤖 Telegram Bot yaratish",
    "srv_web": "🌐 Veb-sayt va CRM",
    "srv_smm": "📈 SMM va Target",
    "srv_design": "🎨 Dizayn va Branding"
}

def get_lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
        ]
    ])

def get_main_reply_keyboard(lang: str):
    t = LANGUAGES.get(lang, LANGUAGES["uz"])
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_services"]), KeyboardButton(text=t["btn_order"])],
            [KeyboardButton(text=t["btn_portfolio"]), KeyboardButton(text=t["btn_website"])],
            [KeyboardButton(text=t["btn_faq"]), KeyboardButton(text=t["btn_contact"])],
            [KeyboardButton(text=t["btn_lang"]), KeyboardButton(text=t["btn_about"])]
        ],
        resize_keyboard=True
    )

def get_multi_services_keyboard(selected_keys: list):
    keyboard = []
    for key, name in ALL_SERVICES.items():
        icon = "✅ " if key in selected_keys else "⬜️ "
        keyboard.append([InlineKeyboardButton(text=f"{icon}{name}", callback_data=f"toggle_{key}")])
    
    keyboard.append([InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_services")])
    keyboard.append([InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")
    t = LANGUAGES[lang]
    await message.answer(t["welcome"], reply_markup=get_lang_keyboard(), parse_mode=ParseMode.HTML)

@router.callback_query(F.data.startswith("lang_"))
async def set_language_cb(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    user_languages[callback.from_user.id] = lang
    t = LANGUAGES[lang]
    await state.clear()
    await callback.message.answer(t["menu"], reply_markup=get_main_reply_keyboard(lang), parse_mode=ParseMode.HTML)
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.answer()

# --- REPLY KEYBOARD HANDLERS ---
@router.message(F.text.in_(["🌐 Tilni o'zgartirish / Language", "🌐 Сменить язык / Language"]))
async def reply_change_lang(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Tilni tanlang / Выберите язык:", reply_markup=get_lang_keyboard())

@router.message(F.text.in_(["🛍 Mahsulotlar & Xizmatlar", "🛍 Продукты и Услуги"]))
async def reply_services(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Saytda narxlar bilan tanishish", url=WEBSITE_URL)]
    ])
    await message.answer(t["services"], reply_markup=kb, parse_mode=ParseMode.HTML)

@router.message(F.text.in_(["🖼 Portfolio galereyasi", "🖼 Портфолио"]))
async def reply_portfolio(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Portfolio kanaliga o'tish", url=PORTFOLIO_CHANNEL_URL)]
    ])
    await message.answer(t["portfolio"], reply_markup=kb, parse_mode=ParseMode.HTML)

@router.message(F.text.in_(["❓ Ko'p beriladigan savollar", "❓ FAQ"]))
async def reply_faq(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    await message.answer(t["faq"], parse_mode=ParseMode.HTML)

@router.message(F.text.in_(["ℹ️ Ma'lumot", "ℹ️ Информация"]))
async def reply_about(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    await message.answer(t["about"], parse_mode=ParseMode.HTML)

@router.message(F.text.in_(["🌐 Veb-sayt", "🌐 Веб-сайт"]))
async def reply_website(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Saytga o'tish", url=WEBSITE_URL)]
    ])
    await message.answer(t["website"], reply_markup=kb, parse_mode=ParseMode.HTML)

@router.message(F.text.in_(["📞 Biz bilan bog'lanish", "📞 Контакты"]))
async def reply_contact(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    await message.answer(t["contact"], parse_mode=ParseMode.HTML)

@router.message(F.text.in_(["🚀 Buyurtma berish", "🚀 Сделать заказ"]))
async def reply_order(message: Message, state: FSMContext):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    await state.set_state(OrderState.waiting_for_name)
    await message.answer(t["order_name"], parse_mode=ParseMode.HTML)


# --- FSM: BUYURTMA JARAYONI ---
@router.message(OrderState.waiting_for_name, ~F.text)
async def process_name_invalid_type(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    await message.answer(t["invalid_name"])

@router.message(OrderState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    
    name_pattern = re.compile(r"^[a-zA-Zà-üÀ-Ü ']+$")
    if not name_pattern.match(message.text.strip()) or len(message.text.strip()) < 2:
        await message.answer(t["invalid_name"])
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(OrderState.waiting_for_phone)
    await message.answer(t["order_phone"].format(name=message.text.strip()), parse_mode=ParseMode.HTML)

@router.message(OrderState.waiting_for_phone, ~F.text)
async def process_phone_invalid_type(message: Message):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]
    await message.answer(t["invalid_phone"])

@router.message(OrderState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    lang = user_languages.get(message.from_user.id, "uz")
    t = LANGUAGES[lang]

    phone_pattern = re.compile(r"^\+?[0-9]{9,15}$")
    clean_phone = message.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    
    if not phone_pattern.match(clean_phone):
        await message.answer(t["invalid_phone"])
        return

    await state.update_data(phone=message.text.strip(), clean_phone=clean_phone)
    
    user_id = message.from_user.id
    user_selected_services[user_id] = []
    
    await state.set_state(OrderState.waiting_for_services)
    await message.answer(t["select_services"], reply_markup=get_multi_services_keyboard([]), parse_mode=ParseMode.HTML)

@router.callback_query(OrderState.waiting_for_services, F.data.startswith("toggle_"))
async def toggle_service_selection(callback: CallbackQuery):
    user_id = callback.from_user.id
    service_key = callback.data.replace("toggle_", "")
    
    if user_id not in user_selected_services:
        user_selected_services[user_id] = []
        
    if service_key in user_selected_services[user_id]:
        user_selected_services[user_id].remove(service_key)
    else:
        user_selected_services[user_id].append(service_key)
        
    lang = user_languages.get(user_id, "uz")
    t = LANGUAGES[lang]
    
    try:
        await callback.message.edit_text(
            t["select_services"],
            reply_markup=get_multi_services_keyboard(user_selected_services[user_id]),
            parse_mode=ParseMode.HTML
        )
    except Exception:
        pass
    await callback.answer()

@router.callback_query(OrderState.waiting_for_services, F.data == "confirm_services")
async def confirm_selected_services(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "uz")
    t = LANGUAGES[lang]
    
    selected_keys = user_selected_services.get(user_id, [])
    if not selected_keys:
        await callback.answer(t["no_services_selected"], show_alert=True)
        return
        
    service_names_list = [ALL_SERVICES[k] for k in selected_keys if k in ALL_SERVICES]
    services_text = ", ".join(service_names_list)
    
    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    clean_phone = data.get("clean_phone")
    username = f"@{callback.from_user.username}" if callback.from_user.username else "Mavjud emas"

    global client_counter
    client_counter += 1

    promo_text = ""
    user_bonus_text = ""
    
    if client_counter <= 3:
        assigned_bonus = random.choice(RANDOM_BONUSES)
        promo_text = f"\n\n🎁 <b>OMADLI MIJOZ (#{client_counter}):</b>\n{assigned_bonus}"
        user_bonus_text = f"\n\n🎉 <b>Tabriklaymiz!</b> Siz bizning dastlabki 3 ta omadli mijozimiz qatoriga kirdingiz va sizga maxsus sovg'a taqdim etildi:\n<b>{assigned_bonus}</b>"

    channel_msg = (
        f"🔔 <b>Yangi Buyurtma (#{client_counter})!</b>\n\n"
        f"🛍 <b>Xizmatlar:</b> {html.quote(services_text)}\n"
        f"👤 <b>Ism:</b> {html.quote(name)}\n"
        f"📞 <b>Telefon:</b> <a href='tel:{clean_phone}'>{html.quote(phone)}</a>\n"
        f"🔗 <b>Telegram:</b> <a href='tg://user?id={user_id}'>{username}</a>\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>"
        f"{promo_text}"
    )

    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"order_accept_{user_id}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"order_cancel_{user_id}")
        ]
    ])

    try:
        await bot.send_message(
            chat_id=ADMIN_CHANNEL_ID,
            text=channel_msg,
            reply_markup=admin_kb,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logging.error(f"Kanalga xabar yuborishda xatolik: {e}")

    pay_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Xavfsiz To'lovga O'tish", url=PAYMENT_LINK)],
        [InlineKeyboardButton(text="🔙 Asosiy Menyu", callback_data="back_main")]
    ])

    final_user_message = t["order_pending"] + user_bonus_text
    await callback.message.answer(final_user_message, reply_markup=pay_kb, parse_mode=ParseMode.HTML)
    await state.clear()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.answer()

@router.callback_query(F.data == "back_main")
async def cb_back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = user_languages.get(callback.from_user.id, "uz")
    t = LANGUAGES[lang]
    await callback.message.answer(t["menu"], reply_markup=get_main_reply_keyboard(lang), parse_mode=ParseMode.HTML)
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.answer()

# --- Admin tugmalari: Qabul qilish yoki Rad etish ---
@router.callback_query(F.data.startswith("order_"))
async def handle_order_action(callback: CallbackQuery, bot: Bot):
    parts = callback.data.split("_")
    action = parts[1]
    user_id = int(parts[2])
    
    original_text = callback.message.text
    
    if action == "accept":
        new_text = original_text + "\n\n<b>STATUS:</b> ✅ Buyurtma tasdiqlandi (50% avans kutilmoqda)"
    else:
        new_text = original_text + "\n\n<b>STATUS:</b> ❌ Buyurtma rad etildi"
        try:
            await bot.send_message(chat_id=user_id, text="❌ Kechirasiz, hozirgi vaqtda buyurtmangiz rad etildi.", parse_mode=ParseMode.HTML)
        except Exception:
            pass
        
    try:
        await callback.message.edit_text(new_text, parse_mode=ParseMode.HTML)
    except Exception:
        pass
    await callback.answer("Buyurtma holati yangilandi!")

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    print("Mega bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())