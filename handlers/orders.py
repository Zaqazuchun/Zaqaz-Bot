from aiogram import Router, F
from aiogram.types import CallbackQuery
import database

router = Router()

@router.callback_query(F.data == "start_order")
async def start_order(callback: CallbackQuery):

    async with database.pool.acquire() as conn:
        products = await conn.fetch(
            "SELECT id, name, price FROM products WHERE active=TRUE"
        )

    if not products:
        await callback.message.answer("📭 Hozir mahsulot yo‘q")
        await callback.answer()
        return

    text = "🛍 <b>Katalog:</b>\n\n"

    for p in products:
        text += f"{p['id']}. {p['name']} — {p['price']} so‘m\n"

    await callback.message.answer(text)
    await callback.answer()