from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards.main_menu import main_menu_keyboard

from aiogram.types import ReplyKeyboardRemove

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Удаляем старую ReplyKeyboard
    await message.answer(
        "🔄 Обновляю меню...",
        reply_markup=ReplyKeyboardRemove()
    )

    # Отправляем новое сообщение с инлайн-клавиатурой
    await message.answer(
        "Добро пожаловать в ресторан Debassus!",
        reply_markup=main_menu_keyboard
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в ресторан Debassus!",
        reply_markup=main_menu_keyboard
    )