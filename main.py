
import os
import asyncio
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Booking(StatesGroup):
    language = State()
    program = State()
    format = State()
    date = State()
    time = State()
    name = State()
    phone = State()
    confirm = State()

TEXT = {
    "ru": {
        "welcome": (
            "🤍 <b>Bonne Forme — Pilates Studio</b>\n\n"
            "Демо Telegram-бота для записи и работы с клиентами.\n"
            "Здесь клиент может выбрать направление, формат занятия, время и оставить заявку без переписки с администратором."
        ),
        "menu_book": "📅 Записаться",
        "menu_programs": "🧘 Направления",
        "menu_packages": "🎟 Абонементы",
        "menu_about": "✨ О Bonne Forme",
        "menu_contact": "📞 Контакты",
        "choose_program": "Выберите направление:",
        "choose_format": "Выберите формат занятия:",
        "choose_date": "Выберите удобный день:",
        "choose_time": "Выберите время:",
        "ask_name": "Как вас зовут?",
        "ask_phone": "Оставьте номер телефона для подтверждения записи:",
        "confirm_title": "Проверьте заявку:",
        "confirm_btn": "✅ Подтвердить",
        "cancel_btn": "❌ Отменить",
        "done": (
            "✅ <b>Заявка принята!</b>\n\n"
            "В рабочей версии администратор Bonne Forme сразу получит эту заявку.\n"
            "Клиенту можно автоматически отправить подтверждение и напоминание перед занятием.\n\n"
            "ℹ️ Это демонстрационная версия."
        ),
        "cancelled": "Заявка отменена.",
        "programs_text": (
            "🧘 <b>Направления Bonne Forme</b>\n\n"
            "• Pilates Reformer / профессиональное оборудование\n"
            "• Индивидуальные занятия\n"
            "• Групповые занятия\n"
            "• Prenatal / Postnatal\n"
            "• Онлайн-занятия\n\n"
            "В полноценной версии список можно синхронизировать с актуальными услугами студии."
        ),
        "packages_text": (
            "🎟 <b>Абонементы</b>\n\n"
            "В рабочей версии здесь можно показать реальные пакеты, остаток занятий клиента "
            "и кнопку «Продлить».\n\n"
            "Бот также может напоминать об окончании пакета заранее."
        ),
        "about_text": (
            "✨ <b>Bonne Forme</b>\n\n"
            "Сеть Pilates-студий с профессиональным оборудованием и квалифицированными инструкторами.\n\n"
            "В демо мы показываем, как Telegram может стать дополнительным каналом записи и удержания клиентов."
        ),
        "contact_text": (
            "📞 <b>Контакты</b>\n\n"
            "Сайт: pilatesbonneforme.com\n"
            "Кишинёв, Республика Молдова\n\n"
            "В рабочей версии можно добавить все 4 студии, карту, телефоны и быстрый выбор филиала."
        ),
        "back": "⬅️ В меню",
    },
    "ro": {
        "welcome": (
            "🤍 <b>Bonne Forme — Pilates Studio</b>\n\n"
            "Demo de bot Telegram pentru programări și comunicarea cu clienții.\n"
            "Clientul poate alege programul, tipul ședinței, ora și poate trimite cererea fără conversații lungi cu administratorul."
        ),
        "menu_book": "📅 Programează-te",
        "menu_programs": "🧘 Programe",
        "menu_packages": "🎟 Abonamente",
        "menu_about": "✨ Despre Bonne Forme",
        "menu_contact": "📞 Contacte",
        "choose_program": "Alege programul:",
        "choose_format": "Alege formatul ședinței:",
        "choose_date": "Alege ziua potrivită:",
        "choose_time": "Alege ora:",
        "ask_name": "Cum te numești?",
        "ask_phone": "Lasă numărul de telefon pentru confirmarea programării:",
        "confirm_title": "Verifică cererea:",
        "confirm_btn": "✅ Confirmă",
        "cancel_btn": "❌ Anulează",
        "done": (
            "✅ <b>Cererea a fost trimisă!</b>\n\n"
            "În versiunea finală, administratorul Bonne Forme primește imediat această cerere.\n"
            "Clientului i se poate trimite automat confirmarea și un reminder înainte de ședință.\n\n"
            "ℹ️ Aceasta este o versiune demo."
        ),
        "cancelled": "Cererea a fost anulată.",
        "programs_text": (
            "🧘 <b>Programe Bonne Forme</b>\n\n"
            "• Pilates Reformer / echipamente profesionale\n"
            "• Ședințe individuale\n"
            "• Ședințe de grup\n"
            "• Prenatal / Postnatal\n"
            "• Online\n\n"
            "În versiunea finală, lista poate fi sincronizată cu serviciile actuale ale studioului."
        ),
        "packages_text": (
            "🎟 <b>Abonamente</b>\n\n"
            "În versiunea finală aici pot apărea pachetele reale, numărul de ședințe rămase "
            "și butonul „Prelungește”.\n\n"
            "Botul poate trimite și remindere înainte de expirarea pachetului."
        ),
        "about_text": (
            "✨ <b>Bonne Forme</b>\n\n"
            "Rețea de studiouri Pilates cu echipamente profesionale și instructori calificați.\n\n"
            "Demo-ul arată cum Telegram poate deveni un canal suplimentar pentru programări și retenția clienților."
        ),
        "contact_text": (
            "📞 <b>Contacte</b>\n\n"
            "Site: pilatesbonneforme.com\n"
            "Chișinău, Republica Moldova\n\n"
            "În versiunea finală se pot adăuga toate cele 4 studiouri, harta, telefoanele și alegerea rapidă a locației."
        ),
        "back": "⬅️ Meniu",
    }
}

PROGRAMS = {
    "reformer": {"ru": "Pilates Reformer", "ro": "Pilates Reformer"},
    "group": {"ru": "Групповое занятие", "ro": "Ședință de grup"},
    "individual": {"ru": "Индивидуальное занятие", "ro": "Ședință individuală"},
    "prenatal": {"ru": "Prenatal / Postnatal", "ro": "Prenatal / Postnatal"},
    "online": {"ru": "Онлайн-занятие", "ro": "Ședință online"},
}
FORMATS = {
    "trial": {"ru": "Пробное занятие", "ro": "Ședință de probă"},
    "regular": {"ru": "Обычное занятие", "ro": "Ședință obișnuită"},
    "consult": {"ru": "Нужна консультация", "ro": "Am nevoie de consultație"},
}
SLOTS = ["08:00", "10:00", "12:00", "17:00", "19:00"]

def t(lang, key):
    return TEXT[lang][key]

def lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇴 Română", callback_data="lang:ro"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        ]
    ])

def menu_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "menu_book"), callback_data="menu:book")],
        [
            InlineKeyboardButton(text=t(lang, "menu_programs"), callback_data="menu:programs"),
            InlineKeyboardButton(text=t(lang, "menu_packages"), callback_data="menu:packages"),
        ],
        [
            InlineKeyboardButton(text=t(lang, "menu_about"), callback_data="menu:about"),
            InlineKeyboardButton(text=t(lang, "menu_contact"), callback_data="menu:contact"),
        ],
        [InlineKeyboardButton(text="🌐 RO / RU", callback_data="menu:language")]
    ])

def back_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="menu:home")]
    ])

def programs_kb(lang):
    rows = []
    for key, labels in PROGRAMS.items():
        rows.append([InlineKeyboardButton(text=labels[lang], callback_data=f"program:{key}")])
    rows.append([InlineKeyboardButton(text=t(lang, "back"), callback_data="menu:home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def formats_kb(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=v[lang], callback_data=f"format:{k}")]
        for k, v in FORMATS.items()
    ])

def dates_kb(lang):
    today = datetime.now()
    rows = []
    day_names_ro = ["Lun", "Mar", "Mie", "Joi", "Vin", "Sâm", "Dum"]
    day_names_ru = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    names = day_names_ro if lang == "ro" else day_names_ru
    for offset in range(1, 5):
        d = today + timedelta(days=offset)
        label = f"{names[d.weekday()]}, {d.strftime('%d.%m')}"
        rows.append([InlineKeyboardButton(text=label, callback_data=f"date:{d.strftime('%Y-%m-%d')}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def times_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=s, callback_data=f"time:{s}") for s in SLOTS[:3]],
        [InlineKeyboardButton(text=s, callback_data=f"time:{s}") for s in SLOTS[3:]],
    ])

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Alege limba / Выберите язык:",
        reply_markup=lang_kb()
    )

@dp.callback_query(F.data.startswith("lang:"))
async def choose_lang(call: CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[1]
    await state.update_data(lang=lang)
    await call.message.edit_text(
        t(lang, "welcome"),
        reply_markup=menu_kb(lang),
        parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data == "menu:language")
async def change_lang(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Alege limba / Выберите язык:", reply_markup=lang_kb())
    await call.answer()

@dp.callback_query(F.data == "menu:home")
async def home(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await call.message.edit_text(t(lang, "welcome"), reply_markup=menu_kb(lang), parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "menu:programs")
async def programs(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await call.message.edit_text(t(lang, "programs_text"), reply_markup=back_kb(lang), parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "menu:packages")
async def packages(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await call.message.edit_text(t(lang, "packages_text"), reply_markup=back_kb(lang), parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "menu:about")
async def about(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await call.message.edit_text(t(lang, "about_text"), reply_markup=back_kb(lang), parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "menu:contact")
async def contact(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await call.message.edit_text(t(lang, "contact_text"), reply_markup=back_kb(lang), parse_mode="HTML")
    await call.answer()

@dp.callback_query(F.data == "menu:book")
async def book(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await state.set_state(Booking.program)
    await call.message.edit_text(t(lang, "choose_program"), reply_markup=programs_kb(lang))
    await call.answer()

@dp.callback_query(Booking.program, F.data.startswith("program:"))
async def pick_program(call: CallbackQuery, state: FSMContext):
    key = call.data.split(":")[1]
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await state.update_data(program=key)
    await state.set_state(Booking.format)
    await call.message.edit_text(t(lang, "choose_format"), reply_markup=formats_kb(lang))
    await call.answer()

@dp.callback_query(Booking.format, F.data.startswith("format:"))
async def pick_format(call: CallbackQuery, state: FSMContext):
    key = call.data.split(":")[1]
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await state.update_data(format=key)
    await state.set_state(Booking.date)
    await call.message.edit_text(t(lang, "choose_date"), reply_markup=dates_kb(lang))
    await call.answer()

@dp.callback_query(Booking.date, F.data.startswith("date:"))
async def pick_date(call: CallbackQuery, state: FSMContext):
    date = call.data.split(":")[1]
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await state.update_data(date=date)
    await state.set_state(Booking.time)
    await call.message.edit_text(t(lang, "choose_time"), reply_markup=times_kb())
    await call.answer()

@dp.callback_query(Booking.time, F.data.startswith("time:"))
async def pick_time(call: CallbackQuery, state: FSMContext):
    time = call.data.split(":")[1]
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await state.update_data(time=time)
    await state.set_state(Booking.name)
    await call.message.edit_text(t(lang, "ask_name"))
    await call.answer()

@dp.message(Booking.name)
async def get_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await state.update_data(name=message.text.strip())
    await state.set_state(Booking.phone)
    await message.answer(t(lang, "ask_phone"))

@dp.message(Booking.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    data = await state.get_data()
    lang = data.get("lang", "ro")

    program = PROGRAMS[data["program"]][lang]
    fmt = FORMATS[data["format"]][lang]
    summary = (
        f"{t(lang, 'confirm_title')}\n\n"
        f"🧘 {program}\n"
        f"🎯 {fmt}\n"
        f"📅 {data['date']}\n"
        f"🕐 {data['time']}\n"
        f"👤 {data['name']}\n"
        f"📞 {data['phone']}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang, "confirm_btn"), callback_data="booking:confirm"),
            InlineKeyboardButton(text=t(lang, "cancel_btn"), callback_data="booking:cancel")
        ]
    ])
    await state.set_state(Booking.confirm)
    await message.answer(summary, reply_markup=kb, parse_mode="HTML")

@dp.callback_query(Booking.confirm, F.data == "booking:confirm")
async def confirm_booking(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    program = PROGRAMS[data["program"]][lang]
    fmt = FORMATS[data["format"]][lang]

    admin_text = (
        "🆕 DEMO Bonne Forme — новая заявка\n\n"
        f"Язык: {lang.upper()}\n"
        f"Программа: {program}\n"
        f"Формат: {fmt}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}"
    )
    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(ADMIN_CHAT_ID, admin_text)
        except Exception:
            pass

    await call.message.edit_text(t(lang, "done"), reply_markup=back_kb(lang), parse_mode="HTML")
    await state.set_state(None)
    await state.update_data(lang=lang)
    await call.answer()

@dp.callback_query(Booking.confirm, F.data == "booking:cancel")
async def cancel_booking(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ro")
    await call.message.edit_text(t(lang, "cancelled"), reply_markup=back_kb(lang))
    await state.set_state(None)
    await state.update_data(lang=lang)
    await call.answer()

async def main():
    print("Bonne Forme demo bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
