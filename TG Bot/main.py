import telebot
from telebot import types

import config
from config import stickerpacks, liveURLs
from info import getTeamInfo, getDriverInfo, getCalendar

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_menu = types.KeyboardButton("Меню 🧾")
    markup.add(button_menu)
    bot.send_message(message.chat.id,
                     text="<b>Привет, {0.first_name}!</b>\nЖми кнопку \"Меню\", чтобы начать работу со мной".format(
                         message.from_user), reply_markup=markup, parse_mode="HTML")
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEGph1jidiYrjUtZsw6JhY6XUMHMZT6awACEyIAAiO60ErugP0LGPd1mysE")


@bot.message_handler(content_types=['text'])
def func(message):
    button_teams = types.KeyboardButton("Команды 🏎")
    button_back = types.KeyboardButton("Меню 🧾")
    button_drivers = types.KeyboardButton("Пилоты 👨‍🚀")
    button_calendar = types.KeyboardButton("Календарь 📆")
    button_stickers = types.KeyboardButton("Стикеры 😁")
    button_live = types.KeyboardButton("Трансляции 📺")
    if (message.text in ["Меню 🧾", "Вернуться в главное меню 🔙", "Меню"]):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(button_calendar, button_stickers, button_teams, button_drivers, button_live)
        bot.send_message(message.chat.id, text="Что вас интересует?", reply_markup=markup)

    elif ((message.text == "Календарь 📆") or (message.text in list(map(str, range(1950, 2100))))):
        if message.text != "Календарь 📆":
            bot.send_message(message.chat.id, f"Одну минутку, сейчас поищу календарь на сезон {message.text}")
            calendar = getCalendar(message.text)
            if calendar != f"<b>Я не нашел календарь Формулы-1 сезона {message.text} 😞</b>\nПопросите его у меня позже, возможно я смогу его вам показать":
                calendar = f"<b>Вот, что мне удалось найти</b> 🕵️‍♂️\n\n\n{getCalendar(message.text)}"
            bot.send_message(message.chat.id, calendar, parse_mode="HTML")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(button_calendar, button_stickers, button_teams, button_drivers)
            bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Введите интересующий вас год")

    elif (message.text == "Стикеры 😁"):
        for sticker in stickerpacks:
            bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id,
                         text="<b>Вот стикерпаки, которые есть в наличии!</b>  🏎\n\nЧтобы добавить их к себе в библиотеку, нажми на любой из понравившихся стикеров и используй кнопку <b>\"Добавить стикеры\"</b>",
                         parse_mode="HTML")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(button_calendar, button_stickers, button_teams, button_drivers)
        bot.send_message(message.chat.id, text="Выберите действие", reply_markup=markup)

    elif (message.text == "Команды 🏎"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        team_buttons = [types.KeyboardButton(f"{team}") for team in config.teamURLs.keys()]
        for team in range(len(team_buttons)):
            markup.add(team_buttons[team], row_width=2)
        markup.add(button_back, row_width=2)
        bot.send_message(message.chat.id, text="Какой коллектив вас интересует?", reply_markup=markup)
    elif (message.text in config.teamURLs.keys()):
        teamInfo = getTeamInfo(config.teamURLs.get(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button_Driver1 = types.KeyboardButton(f"{teamInfo[2]}")
        button_Driver2 = types.KeyboardButton(f"{teamInfo[3]}")
        markup.add(button_Driver1, button_Driver2, button_teams, button_back)
        bot.send_photo(message.chat.id, photo=open(f"teamPics/{teamInfo[1]}.jpg", 'rb'), caption=teamInfo[0], parse_mode='HTML')
        bot.send_message(message.chat.id, text=f"Хотите узнать подробнее о пилотах <b>{teamInfo[1]}</b>?",
                         reply_markup=markup, parse_mode='HTML')
    elif (message.text in config.driverURLs.keys()):
        driverInfo = getDriverInfo(config.driverURLs.get(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(button_teams, button_drivers, button_back)
        bot.send_photo(message.chat.id, photo=open(f"driverPics/{driverInfo[1]}.jpg", 'rb'), caption=driverInfo[0], parse_mode='HTML', reply_markup=markup)
    elif (message.text == "Пилоты 👨‍🚀"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        driver_buttons = [types.KeyboardButton(f"{driver}") for driver in config.driverURLs.keys()]
        for driver in range(len(driver_buttons)):
            markup.add(driver_buttons[driver], row_width=2)
        markup.add(button_back, row_width=2)
        bot.send_message(message.chat.id, text="Какой пилот вас интересует?", reply_markup=markup)
    elif (message.text == "Трансляции 📺"):
        markup = types.InlineKeyboardMarkup()
        live_buttons = [types.InlineKeyboardButton(text=f"{liveURL[0]}", url=f"{liveURL[1]}") for liveURL in liveURLs]
        for button in live_buttons:
            markup.add(button, row_width=2)
        bot.send_message(message.chat.id, "<b>Где можно посмотреть Формулу-1? 📺</b>\n\nНиже представлены кнопки, ведущие на ресурсы с качественными прямыми трансляциями гоночных уик-эндов", reply_markup=markup, parse_mode='HTML')

    else:
        bot.send_message(message.chat.id, text="Простие, я вас не понимаю 😔")


bot.polling(none_stop=True)
