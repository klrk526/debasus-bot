import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from dotenv import load_dotenv

load_dotenv()


# ⚠️ ВСТАВЬ СЮДА СВОЙ НОВЫЙ ТОКЕН (старый скомпрометирован, его нужно отозвать в @BotFather через /revoke)
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# СОСТОЯНИЯ ДЛЯ БРОНИРОВАНИЯ (FSM)
# ==========================================
class BookingStates(StatesGroup):
    waiting_for_guests = State()
    waiting_for_time = State()
    waiting_for_phone = State()
    waiting_for_surname = State()

# ==========================================
# БАЗА ДАННЫХ АКЦИЙ
# ==========================================
DAILY_PROMOS = {
    1: "🍕 <b>Понедельник — Сорт пива за пол цены!</b>\n\nЗаказывайте пиво и платите за него полцены!",
    2: "🍔 <b>Вторник — Пивной безлимит!</b>\n\nПокупай безлимит и пей пиво до 22:00",
    3: "🍝 <b>Среда — Безлимит на игристое вино!</b>\n\nПокупай безлимит и пей игристое вино сколько хочешь",
    4: "🍻 <b>Четверг — Акция на настойки</b>\n\nНастойки по специальной цене",
    5: "🍷 <b>Пятница — Сет настоек в подарок!</b>\n\nПриходите большой компанией и получите подарок - сет настоек",
    6: "🥩 <b>Суббота — Сет настоек в подарок!</b>\n\nПриходите большой компанией и получите подарок - сет настоек",
    0: "🥂 <b>Воскресенье — Акция на кухню!</b>\n\nВесь день скидка 20% на все позиции кухни!"
}

def get_today_promo():
    today = datetime.now().weekday()
    promo_key = today + 1 if today < 6 else 0
    return DAILY_PROMOS.get(promo_key, "Сегодня нет специальных акций, но основное меню всегда великолепно!")


# ==========================================
# ОБРАБОТЧИКИ КОМАНД
# ==========================================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Акции сегодня", callback_data="promo_today")],
        [InlineKeyboardButton(text="📍 Как нас найти", callback_data="location")],
        [InlineKeyboardButton(text="📞 Забронировать стол", callback_data="booking")]
    ])

    await message.answer(
        f"👋 Приветствуем в ресторане <b>«Дебассус»</b> (Воронеж)!\n\n"
        f"Я ваш виртуальный помощник. Здесь вы можете узнать о самых вкусных предложениях дня и забронировать столик.\n\n"
        f"Выберите действие:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав администратора.")
        return
    await message.answer("Привет, админиистратор!")


@dp.callback_query(F.data == "promo_today")
async def show_promo(callback: CallbackQuery):
    promo_text = get_today_promo()
    await callback.message.edit_text(
        text=f"{promo_text}\n\n<i>Акция действует только сегодня! Успейте забронировать столик.</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data == "location")
async def show_location(callback: CallbackQuery):
    await callback.message.edit_text(
        text="📍 <b>Наш адрес:</b>\n"
             "г. Воронеж, ул. Бул.Победы, д. 12А\n\n"
             "🚇 Удобно добраться от любой точки города.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# === НАЧАЛО БРОНИРОВАНИЯ ===
@dp.callback_query(F.data == "booking")
async def start_booking(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingStates.waiting_for_guests)
    await callback.message.edit_text(
        text="🍽️ <b>Бронирование столика</b>\n\n"
             "Давайте заполним данные. <b>Шаг 1/4:</b>\n"
             "Напишите количество гостей цифрой (например: 2 или 5)",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
        ])
    )
    await callback.answer()


# === ШАГ 1: ВВОД КОЛИЧЕСТВА ГОСТЕЙ (ТЕКСТОМ) ===
@dp.message(BookingStates.waiting_for_guests)
async def process_guests(message: Message, state: FSMContext):
    guests_text = message.text.strip()

    # Проверяем, что введены только цифры
    if not guests_text.isdigit():
        await message.answer(
            "❌ Пожалуйста, введите число.\n\n"
            "Например: <b>2</b> или <b>4</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
            ])
        )
        return

    guests = int(guests_text)

    # Проверяем разумный диапазон (от 1 до 50 человек)
    if not (1 <= guests <= 50):
        await message.answer(
            "❌ Укажите корректное количество гостей (от 1 до 50).",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
            ])
        )
        return

    # Сохраняем данные и переходим к следующему шагу
    await state.update_data(guests=guests)
    await message.answer(
        f"✅ Принято: {guests} гостей\n\n"
        f"<b>Шаг 2/4:</b> На какое время забронировать стол?\n"
        f"Напишите время в формате <b>ЧЧ:ММ</b> (например: 18:30)",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
        ])
    )
    await state.set_state(BookingStates.waiting_for_time)


# === ШАГ 2: ВВОД ВРЕМЕНИ ===
@dp.message(BookingStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    time_text = message.text.strip()
    try:
        hour, minute = map(int, time_text.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except:
        await message.answer(
            "❌ Неверный формат. Пожалуйста, введите время как <b>18:30</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
            ])
        )
        return

    await state.update_data(time=time_text)
    await message.answer(
        f"✅ Принято: {time_text}\n\n"
        f"<b>Шаг 3/4:</b> Ваш номер телефона для связи\n"
        f"(например: +79991234567)",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
        ])
    )
    await state.set_state(BookingStates.waiting_for_phone)


# === ШАГ 3: ВВОД ТЕЛЕФОНА ===
@dp.message(BookingStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    digits = ''.join(filter(str.isdigit, phone))

    if len(digits) not in [10, 11]:
        await message.answer(
            "❌ Неверный номер. Введите корректный номер телефона (10 или 11 цифр).",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
            ])
        )
        return

    await state.update_data(phone=phone)
    await message.answer(
        f"✅ Принято: {phone}\n\n"
        f"<b>Шаг 4/4:</b> Ваша фамилия",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
        ])
    )
    await state.set_state(BookingStates.waiting_for_surname)


# === ШАГ 4: ВВОД ФАМИЛИИ И ФИНАЛ ===
@dp.message(BookingStates.waiting_for_surname)
async def process_surname(message: Message, state: FSMContext):
    surname = message.text.strip()
    if len(surname) < 2:
        await message.answer(
            "❌ Фамилия слишком короткая. Попробуйте еще раз.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_booking")]
            ])
        )
        return

    await state.update_data(surname=surname)
    data = await state.get_data()

    confirmation_text = (
        f"🎉 <b>Бронирование оформлено!</b>\n\n"
        f"📋 <b>Детали:</b>\n"
        f"👥 Гостей: {data['guests']}\n"
        f"🕐 Время: {data['time']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"👤 Фамилия: {data['surname']}\n\n"
        f"Мы ждём вас в «Дебассус»! Администратор свяжется с вами для подтверждения."
    )

    await message.answer(
        confirmation_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
    )
    await state.clear() # Очищаем состояние после успешного завершения


# === ОТМЕНА БРОНИРОВАНИЯ ===
@dp.callback_query(F.data == "cancel_booking")
async def cancel_booking(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="❌ Бронирование отменено.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# === ВОЗВРАТ В ГЛАВНОЕ МЕНЮ ===
@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Акции сегодня", callback_data="promo_today")],
        [InlineKeyboardButton(text="📍 Как нас найти", callback_data="location")],
        [InlineKeyboardButton(text="📞 Забронировать стол", callback_data="booking")]
    ])
    await callback.message.edit_text(
        text="👋 Главное меню ресторана <b>«Дебассус»</b>. Чем могу помочь?",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await callback.answer()


# ==========================================
# ЗАПУСК БОТА
# ==========================================
async def main():
    print("Бот Дебассус запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")

#черновик бота
