from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from database import pool
from states import AddProduct

router = Router()

def register(dp):
    dp.include_router(router)


@router.callback_query(F.data == "add_product")
async def add_product_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.answer("📛 Mahsulot nomini kiriting:")
    await state.set_state(AddProduct.name)

    await callback.answer()  # MUHIM