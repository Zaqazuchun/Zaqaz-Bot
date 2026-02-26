from aiogram.fsm.state import StatesGroup, State

class AddProduct(StatesGroup):
    name = State()
    price = State()

class Cart(StatesGroup):
    choosing = State()