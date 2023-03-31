from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor, types
import requests
import json
import os
import time


TG_API = os.getenv("TG_API")
HELP = """Для запуска бота введи команду <b>/monitoring</b>
Для вызова описания бота: <b>/description</b>"""

previously = "previously.txt"


def get_courses_data() -> float:
    url = f"https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    response_data = json.loads(response.text)

    return response_data["Valute"]["USD"]["Value"]


def save_to_json(data) -> None:
    with open(previously, "a") as f:
        f.write(f"{data} \n")


def main_function(data):
    with open(previously) as file:
        previously_list = file.read().split(" \n")

    previously_USD = float(previously_list[-2])
    if previously_USD == data:
        return "Ничего не изменилось"
    else:
        return f"Курс доллара изменился на: {previously_USD - data}"


# Telegrams body

bot = Bot(TG_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['monitoring'])
async def monitoring_valute(message: types.Message):
    data = get_courses_data()
    save_to_json(data)
    bots_answer = main_function(data)
    print(bots_answer)
    time.sleep(30)

    await message.answer(f"{bots_answer}")


@dp.message_handler(commands=["help"])
async def help_me(message: types.Message):
    await message.answer(HELP, parse_mode="HTML")


while True:
    executor.start_polling(dp)
