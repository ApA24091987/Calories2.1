from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Create ReplyKeyboardMarkup with buttons
keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    types.KeyboardButton('Рассчитать'),
    types.KeyboardButton('Информация')
]
keyboard_markup.add(*buttons)

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет Я бот помогающий твоему здоровью", reply_markup=keyboard_markup)

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer("Введите свой возраст:", reply_markup=types.ReplyKeyboardRemove())
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def formula_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
    await message.answer(f"Ваша суточная норма калорий: {calories:.2f} ккал", reply_markup=keyboard_markup)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
