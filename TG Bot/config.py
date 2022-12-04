token = "5899204719:AAEqnkTQSdt6o7H-NUqPIrm-qBI2eNgRfeI"

import requests
from bs4 import BeautifulSoup
import sqlite3


# Получение актуального списка пилотов
response = requests.get('https://ru.motorsport.com/f1/standings/2022/?type=Team&class=')
bs = BeautifulSoup(response.text, "lxml")
teamURLs = bs.find('table', class_='ms-table ms-table--result').find('tbody').find_all('tr', class_='ms-table_row')

teamURLs = {
    " ".join(team.find_next('span', class_='name').text.split()): "https://ru.motorsport.com/" + team.find_next('a',
                                                                                                                class_='ms-link').get(
        'href') for team in teamURLs}

# Получение актуального списка пилотов
response = requests.get('https://ru.motorsport.com/f1/standings/2022/?type=Driver&class=')
bs = BeautifulSoup(response.text, "lxml")
driverURLs = bs.find('tbody').find_all('tr', class_='ms-table_row')
driverURLs = {
    " ".join(driver.find_next('span', class_='name').text.split()): "https://ru.motorsport.com" + driver.find_next('a',
                                                                                                                   class_='ms-link').get(
        'href') for driver in driverURLs}

# Словарь с флагами стран для вставки в сообщения
flagsEmoji = {"austria": '🇦🇹',
              "australia": '🇦🇺',
              "azerbaijan": '🇦🇿',
              "bahrain": '🇧🇭',
              "belgium": '🇧🇪',
              "brazil": '🇧🇷',
              "united kingdom": '🇬🇧',
              "uk": '🇬🇧',
              "hungary": '🇭🇺',
              "vietnam": '🇻🇳',
              "germany": '🇩🇪',
              "great britain": '🇬🇧',
              "denmark": '🇩🇰',
              "israel": '🇮🇱',
              "spain": '🇪🇸',
              "italy": '🇮🇹',
              "canada": '🇨🇦',
              "quatar": '🇶🇦',
              "china": '🇨🇳',
              "malaysia": '🇲🇾',
              "mexico": '🇲🇽',
              "monaco": '🇲🇨',
              "netherlands": '🇳🇱',
              "united arab emirates": '🇦🇪',
              "uae": '🇦🇪',
              "poland": '🇵🇱',
              "russia": '🇷🇺',
              "singapore": '🇸🇬',
              "switzerland": '🇨🇭',
              "united states": '🇺🇸',
              "usa": '🇺🇸',
              "thailand": '🇹🇭',
              "turkey": '🇹🇷',
              "finland": '🇫🇮',
              "france": '🇫🇷',
              "estonia": '🇪🇪',
              "japan": '🇯🇵',
              "saudi arabia": '🇸🇦',
              "portugal": '🇵🇹'}
# 🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿

# Массив из ID стикеров в телеграме. Используется по команде "Стикеры"
stickerpacks = ["CAACAgQAAxkBAAEGpfVjidIJ-OJcd-DR84v9DxfcDroY7QAC4wwAAhoPsFGDw8akCh-fgSsE",
                "CAACAgQAAxkBAAEGpfdjidI-ubyQz795-N8YmkV7IDSw-QACBMADAAFD38I1e7lVMhREHDIrBA",
                "CAACAgIAAxkBAAEGpgJjidPAka2s6d8Wxb_KeuPxb6Kg5QACKAQAAnM9WwuOz_wCAi_CtisE",
                "CAACAgIAAxkBAAEGpghjidQLqHhJGcs47Zie2FkantTWoQACMRQAAvZg0Unn9TfgqHmtMSsE",
                "CAACAgIAAxkBAAEGqeFji1BezdE42FHjdQNr18MGqL6OuAACmAIAAlChKwABFcX1V3DG8qcrBA",
                "CAACAgIAAxkBAAEGqeNji1B3qhgcC2WuL-JqcTWe8OKLuAACVRwAAn5byErEJYGTefiyjisE",
                "CAACAgIAAxkBAAEGqCpjipTRnzS8XjwM3Y0RUY3hYyVBfwACohAAAjIeYUmaiUKNu0M0rSsE",
                "CAACAgIAAxkBAAEGqCxjipTcMtauWfE3Hkjq2lnAU0PgAgACFQAD2zEKHZHMCFhP1YM-KwQ",
                "CAACAgIAAxkBAAEGqC5jipTjuCLqnSKLeaBHT374ieEVzQACmRAAAkSqcUhZtbrWSkubxSsE"]

# Ссылки на ресурсы, на которых можно смотреть трансляции
liveURLs = [
    ["Simply Formula", "https://vk.com/simply_formula"],
    ["Be on Edge", "https://vk.com/be_on_edge"],
    ["Topracing", "https://vk.com/top_racing"]

]

# Создание базы данных для хранения информации о сезонах
# db = sqlite3.connect('F1Assistant.db')
#
# cursor = db.cursor()
#
# # cursor.execute("""CREATE TABLE seasons (
# # season text,
# # info text
# # )""")
#
# cursor.execute("INSERT INTO seasons ('2022', 'ahahahah')")
#
# db.commit()
#
# db.close()
