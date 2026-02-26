from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from database import pool
from states import AddProduct

router = Router()

def register(dp):
    dp.include_router(router)


@router.message(F.text == "➕ Mahsulot qo‘shish")
async def add_product_start(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("📛 Mahsulot nomini kiriting:")
    await state.set_state(AddProduct.name)


@router.message(AddProduct.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Narxini kiriting:")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
async def get_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Faqat raqam kiriting")
        return

    data = await state.get_data()

    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO products (name, price) VALUES ($1, $2)",
            data["name"],
            int(message.text)
        )

    await message.answer("✅ Mahsulot qo‘shildi")
    await state.clear()