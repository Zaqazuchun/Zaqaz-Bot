from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import ADMIN_ID
import database

router = Router()


@router.callback_query(F.data == "list_products")
async def list_products(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    async with database.pool.acquire() as conn:
        products = await conn.fetch(
            "SELECT id, name, price FROM products WHERE active=TRUE ORDER BY id DESC"
        )

    if not products:
        await callback.message.answer("📭 Mahsulotlar hozircha mavjud emas.")
        await callback.answer()
        return

    for product in products:
        text = f"📦 {product['name']}\n💰 {product['price']} so‘m"
        await callback.message.answer(text)

    await callback.answer()