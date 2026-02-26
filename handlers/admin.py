from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID

router = Router()

def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦 Mahsulot qo‘shish", callback_data="add_product")
            ],
            [
                InlineKeyboardButton(text="📋 Mahsulotlar", callback_data="list_products")
            ]
        ]
    )

@router.message(F.text == "/start")
async def start_handler(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👨‍💼 Admin panel", reply_markup=admin_menu())
    else:
        await message.answer("🍔 Xush kelibsiz!")