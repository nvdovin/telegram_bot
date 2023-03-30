import os
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor, types
from utils import get_information

API_KEY = os.getenv("TG_TOKEN")
bot = Bot(API_KEY)
dp = Dispatcher(bot)

alphabet = "qwertyuiopasdfghjklzxcvbnm"
DESCRIPTION = """   Этот бот создан чисто в учебных целях. 
Естественно я буду его развивать!"""


@dp.message_handler(commands=["start"])
async def descr_fonction(message: types.Message):
    data = get_information()
    await message.delete()
    await message.answer(f"""**** Saransk **** 
Температура на день:
Ночью: {data["temperature"]["night"]} °C
Утром: {data["temperature"]["morning"]} °C
Днём: {data["temperature"]["day"]} °C
Вечером: {data["temperature"]["evening"]} °C

Средняя температура: {data["avg_temp"]} °C

Осадки: {data["rain"]}""")
    await message.delete()

@dp.message_handler(commands=["description"])
async def help_command(message: types.Message):
    await message.delete()
    await message.answer(f"Этот бот умеет предсказывать погоду в саранске")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.delete()
    await message.answer(f"""/start для того, чтобы воспользоваться ботом.
/help для списка всех доступных команд
/description для описания бота
/donate 79520727211 для доната на Тинькофф
/author TG: @vdovin_na """)

@dp.message_handler()
async def send_random_letter(message: types.Message):
    await message.delete()
    await message.answer(random.choice(string.ascii_letters))

if __name__ == '__main__':
    executor.start_polling(dp)
