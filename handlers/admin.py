from aiogram import F
from aiogram.types import Message
from config import ADMIN_ID
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Mahsulotlar")],
            [KeyboardButton(text="🧾 Buyurtmalar")]
        ],
        resize_keyboard=True
    )


def register(dp):

    @dp.message(F.text == "/start")
    async def start_handler(message: Message):
        if message.from_user.id == ADMIN_ID:
            await message.answer("👨‍💼 Admin panel", reply_markup=admin_menu())
        else:
            await message.answer("🍔 Xush kelibsiz!\nMini App orqali buyurtma bering.")1