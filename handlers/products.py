from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
import database
from states import AddProduct

router = Router()

@router.callback_query(F.data == "add_product")
async def add_product_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.answer("📛 Mahsulot nomini kiriting:")
    await state.set_state(AddProduct.name)
    await callback.answer()


@router.message(AddProduct.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Narxini kiriting:")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
async def get_price(message: Message, state: FSMContext):

    print("🔥 PRICE HANDLER ISHLADI")

    if not message.text.isdigit():
        await message.answer("❗ Faqat raqam kiriting")
        return

    data = await state.get_data()

    print("DATA:", data)

    if database.pool is None:
        await message.answer("❌ Database ulanmagan")
        return

    async with database.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO products (name, price) VALUES ($1, $2)",
            data["name"],
            int(message.text)
        )

    await message.answer("✅ Mahsulot qo‘shildi")
    await state.clear()