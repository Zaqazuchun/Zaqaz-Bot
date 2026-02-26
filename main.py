import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import init_db

from handlers.admin import router as admin_router
from handlers.products import router as products_router
from handlers.orders import router as orders_router
from handlers.products_list import router as products_list_router


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

dp.include_router(admin_router)
dp.include_router(products_router)
dp.include_router(orders_router)
dp.include_router(products_list_router)

async def main():
    await init_db()
    print("🚀 BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())