from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import database

router = Router()

# =========================
# CART (temporary memory)
# =========================
cart = {}  # { user_id: { product_id: quantity } }


# =========================
# BUYURTMA BOSHLASH
# =========================
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

    for p in products:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="➕ Qo‘shish",
                        callback_data=f"add_{p['id']}"
                    )
                ]
            ]
        )

        text = f"📦 {p['name']}\n💰 {p['price']} so‘m"
        await callback.message.answer(text, reply_markup=keyboard)

    # Tasdiqlash tugmasi
    confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Tasdiqlash",
                    callback_data="confirm_order"
                )
            ]
        ]
    )

    await callback.message.answer("Savatni tasdiqlang:", reply_markup=confirm_keyboard)

    await callback.answer()


# =========================
# SAVATGA QO‘SHISH
# =========================
@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):

    product_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if user_id not in cart:
        cart[user_id] = {}

    if product_id not in cart[user_id]:
        cart[user_id][product_id] = 0

    cart[user_id][product_id] += 1

    await callback.answer("➕ Qo‘shildi")


# =========================
# BUYURTMANI TASDIQLASH
# =========================
@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery):

    user_id = callback.from_user.id

    if user_id not in cart or not cart[user_id]:
        await callback.message.answer("🛒 Savat bo‘sh")
        await callback.answer()
        return

    total = 0

    async with database.pool.acquire() as conn:

        for product_id, qty in cart[user_id].items():

            product = await conn.fetchrow(
                "SELECT price FROM products WHERE id=$1",
                product_id
            )

            total += product["price"] * qty

        await conn.execute(
            "INSERT INTO orders (user_id, total, status) VALUES ($1, $2, $3)",
            user_id,
            total,
            "pending"
        )

    cart[user_id] = {}

    await callback.message.answer(
        f"✅ Buyurtma qabul qilindi\n💰 Jami: {total} so‘m"
    )

    await callback.answer()