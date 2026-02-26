from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import pool
from config import ADMIN_ID

router = Router()


# 📋 Mahsulotlar ro‘yxati tugmasi
@router.callback_query(F.data == "list_products")
async def list_products(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    async with pool.acquire() as conn:
        products = await conn.fetch("SELECT id, name, price FROM products ORDER BY id DESC")

    if not products:
        await callback.message.answer("❌ Mahsulotlar mavjud emas")
        await callback.answer()
        return

    for product in products:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ O‘chirish",
                        callback_data=f"delete_product_{product['id']}"
                    )
                ]
            ]
        )

        text = f"📦 {product['name']}\n💰 {product['price']} so‘m"
        await callback.message.answer(text, reply_markup=keyboard)

    await callback.answer()


# ❌ O‘chirish
@router.callback_query(F.data.startswith("delete_product_"))
async def delete_product(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    product_id = int(callback.data.split("_")[-1])

    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM products WHERE id=$1", product_id)

    await callback.message.edit_text("✅ Mahsulot o‘chirildi")
    await callback.answer()