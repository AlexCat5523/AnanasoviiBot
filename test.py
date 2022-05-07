import requests
import json


# bot = telebot.TeleBot('5384113372:AAHEKO14NhExcv-V7VWeaW2rataUFoo5gtc')   # hlebniimyakishbot


def object_to_find(name):
    # поиск объекта
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    toponym_to_find = name
    city = name.split(', ')[0]

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    json_response = response.json()
    n = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    n = ','.join(n.split())

    # поиск организации
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "Магнит",
        "lang": "ru_RU",
        "ll": n,
        'spn': '0.52,0.52',
        "type": "biz"
    }

    response_org = requests.get(search_api_server, params=search_params)
    json_response_org = response_org.json()

    with open('data/geocoder.json', 'w') as f:
        json.dump(json_response_org, f, ensure_ascii=False)


def find_closest():
    with open('data/geocoder.json') as f:
        data = json.load(f)

        print(f"Ближайший: {data['features'][0]['properties']['description']}")


def find_weather(city):
    AUTH = HTTPBasicAuth('net090906@mail.ru', 'ananas1')  # для подключения к OpenWeather
    forecast_api = 'e9d384fccd160b5870e32f1deb7cd3b8'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={forecast_api}&lang=ru'
    response = requests.get(url)
    json_response = response.json()
    temperature = json_response['main']['temp']
    temperature = round(temperature - 273.1, 1)

    if json_response['weather'][0]['main'] == 'Clouds':
        print(f'Облачно, но можно пойти в магазинчик. Температура: {temperature} \u2103')
    elif json_response['weather'][0]['main'] == 'Rain':
        print(f'Дождь, лучше остаться доме. Температура: {temperature} \u2103')
    elif json_response['weather'][0]['main'] == 'Clear':
        print(f'Солнечно, надо идти в магазинчик. Температура: {temperature} \u2103')
    elif json_response['weather'][0]['main'] == 'Snow':
        print(f'Снег, но можно сходить в магазин. Температура: {temperature} \u2103')


object_to_find('Сочи, улица Волжская, 70')
find_closest()
find_weather('Сочи')

# pos = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
# print(pos)
