import requests
import json
import os
import datetime

weather_link = "https://api.open-meteo.com/v1/forecast?latitude=54.18&longitude=45.17&hourly=temperature_2m,rain&windspeed_unit=ms&precipitation_unit=inch&forecast_days=1&timezone=Europe%2FMoscow"
history = "history.txt"
date = datetime.datetime.now()
print(date)


def get_information():
    weather = requests.get(weather_link).json()
    data = {"rain": []}

    timezone = weather["timezone"]
    temperature = {"night": weather["hourly"]["temperature_2m"][0],
                   "morning": weather["hourly"]["temperature_2m"][5],
                   "day": weather["hourly"]["temperature_2m"][11],
                   "evening": weather["hourly"]["temperature_2m"][17]}

    rain = {"night": weather["hourly"]["rain"][0],
            "morning": weather["hourly"]["rain"][5],
            "day": weather["hourly"]["rain"][11],
            "evening": weather["hourly"]["rain"][17]}

    data["timezone"] = timezone
    data["temperature"] = temperature

    temp_list = [temp for temp in temperature.values()]
    data["avg_temp"] = round(sum(temp_list) / len(temp_list), 2)

    rain_list = [r for r in rain.values()]
    if sum(rain_list) == 0:
        data["rain"] = "Осадков нет"
    else:
        for time, rains in rain:
            data["rain"][time] = rains

    return data


def to_json_file(data) -> None:
    if os.stat(history).st_size == 0:
        with open(history, "a") as f:
            json.dump([data], f)

    else:
        with open(history) as json_file:
            data_list = json.load(json_file)
        data_list.append(data)

        with open(history, "w") as json_file:
            json.dump(data_list, json_file)



def main() -> None:
    """  """
    data = get_information()
    print(f"""
****{data["timezone"]}****

Температура на день:
Ночью: {data["temperature"]["night"]} °C
Утром: {data["temperature"]["morning"]} °C
Днём: {data["temperature"]["day"]} °C
Вечером: {data["temperature"]["evening"]} °C

Средняя температура: {data["avg_temp"]} °C

Осадки: {data["rain"]}""")

    to_json_file(data)


main()
