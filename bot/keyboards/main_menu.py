from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.config import settings
main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🍽 Меню", url=settings.menu_url),
        InlineKeyboardButton(text="🔥 Акции дня", callback_data="promo"),
    ],
    [
        InlineKeyboardButton(text="📅 Забронировать столик", callback_data="booking"),
    ],
    [
        InlineKeyboardButton(text="ℹ️ О ресторане", callback_data="about"),
        InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
    ],
])