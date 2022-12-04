import os

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

from config import flagsEmoji

translator = Translator()



# TODO сделай таймер до ближайшего Гран-при
# TODO сделай карточки Гран-при (Фотка, название, ссылка на интерактивную гугл-карту)
#
# def timeBeforeNextGP(url):
#     responce = requests.get(url)
#     bs = BeautifulSoup(responce.text, 'lxml')
#     timeBeforeGP = [" ".join(bs.find('div', class_='headmenuredr').text.split()[:2]), bs.find('div', class_='timer')]
#     print(timeBeforeGP)
#
# timeBeforeNextGP('https://www.f1-world.ru/teams/list.php3')

def getCalendar(year):
    responce = requests.get(f'https://ru.motorsport.com/f1/schedule/{year}')
    bs = BeautifulSoup(responce.text, 'lxml')
    try:
        GP_Links = bs.find('table', class_='ms-schedule-table ms-schedule-table--your').find_all('tbody')
    except AttributeError:
        calendar = f"<b>Я не нашел календарь Формулы-1 сезона {year} 😞</b>\nПопросите его у меня позже, возможно я смогу его вам показать"
        return calendar
    GP_Links = ["https://ru.motorsport.com" + i.find_next('a').get('href') for i in GP_Links]
    GPs = []
    for link in GP_Links:
        responce = requests.get(link)
        bs = BeautifulSoup(responce.text, 'lxml')
        try:
            GP_Info = [
                " ".join(bs.find('div', class_='ms-entity-header_wrapper ms-ml').find('h1').text.split()[:-1]),
                [i.text for i in bs.find_all('span', class_='ms-event-header-period_day')],
                [i.text for i in bs.find_all('span', class_='ms-event-header-period_month')],
                [bs.find('div', class_='ms-event-header_location').find('span').text,
                 bs.find('div', class_='ms-event-header_location').find('a').text],
                bs.find('span', class_='ms-schedule-item_results-title').text,
            ]
            GP_Info = [GP_Info[0], GP_Info[1][0] + " " + GP_Info[2][0], GP_Info[1][1] + " " + GP_Info[2][1],
                       GP_Info[3][0],
                       translator.translate(str(GP_Info[3][0]), dest='en').text.lower(), GP_Info[3][1],
                       GP_Info[
                           4]]  # переопределяю переменную, чтобы все данные были в удобном одномерном списке [Имя мероприятия, дата начала, дата конца, страна, код для флага страны, Трасса, Статус мероприятия]
            GPs.append(GP_Info)
        except AttributeError:
            if (GP_Links.index(link) + 1) != len(GP_Links):
                continue
            else:
                if len(GPs) != 0:
                    for GP in GPs:
                        calendar += f"\n{GPs.index(GP) + 1}.  <b>{GP[0]}</b>    {GP[1]} — {GP[2]}" \
                                    f"\n    {len(str(GPs.index(GP) + 1)) ** 2 * ' '}<b>Страна:</b> {GP[3]} {flagsEmoji.get(GP[4])}" \
                                    f"\n    {len(str(GPs.index(GP) + 1)) ** 2 * ' '}<b>Трасса:</b> {GP[5]}" \
                                    f"\n    {len(str(GPs.index(GP) + 1)) ** 2 * ' '}<b>Статус:</b> {GP[6]}\n"
                    return calendar
                else:
                    calendar = f"<b>Я не нашел календарь Формулы-1 сезона {year} 😞</b>\nПопросите его у меня позже, возможно я смогу его вам показать"
                    return calendar
        calendar = f"<b>Календарь сезона Формулы-1 {year}:</b>\n"
    for GP in GPs:
        calendar += f"\n{GPs.index(GP) + 1}.  <b>{GP[0]}</b>    {GP[1]} — {GP[2]}" \
                    f"\n    {len(str(GPs.index(GP) + 1))**2*' '}<b>Страна:</b> {GP[3]} {flagsEmoji.get(GP[4])}" \
                    f"\n    {len(str(GPs.index(GP) + 1))**2*' '}<b>Трасса:</b> {GP[5]}" \
                    f"\n    {len(str(GPs.index(GP) + 1))**2*' '}<b>Статус:</b> {GP[6]}\n"
    return calendar


# print(getCalendar(2018))

def getTeamInfo(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    teamName = bs.find('div', class_='ms-entity-header_title-wrapper').find('div').find('h1',
                                                                                        class_='ms-entity-header_title').text
    teamCountry = translator.translate(bs.find('div', class_='ms-entity-header_title-wrapper').find('img').get('title'),
                                       dest='ru').text
    teamDrivers = bs.find('div', class_='ms-grid-vert-drivers-1-2').find_all('div', class_='ms-item_info')
    for i in teamDrivers:
        teamDrivers[teamDrivers.index(i)] = [i.find('a', class_='ms-item_link').get('href'),
                                             " ".join((i.find('a', class_='ms-item_link').text).split()),
                                             i.find('span', class_="ms-item-driver_number").text,
                                             ]
    teamLogo = bs.find('div', class_='ms-entity-header_img-wrapper').find('img',
                                                                          class_='ms-item_img ms-item_img--3_2').get(


        'src')
    if not os.path.exists('teamPics/'):
        os.mkdir('teamPics/')
    imageData = requests.get(teamLogo, verify=False).content
    with open('teamPics/' + teamName + '.jpg', 'wb') as handler:
        handler.write(imageData)
    info = (f'<b>{teamName}</b>\n\n'
            f"<b>Страна</b>: {teamCountry} {flagsEmoji.get(str(translator.translate(teamCountry, dest='en').text).lower())}\n"
            f'<b>Пилоты:</b> {teamDrivers[0][1]} <b>№{teamDrivers[0][2]}</b>, {teamDrivers[1][1]} <b>№{teamDrivers[1][2]}</b>')
    return [info, teamName, f"{teamDrivers[0][1]}", f"{teamDrivers[1][1]}"]


# getTeamInfo('https://ru.motorsport.com/team/red-bull-racing/380/')


def getDriverInfo(url):
    # TODO пропиши количество побед/подиумов/титулов/очков за карьеру
    # /позицию в крайнем сезоне и количество очков в нем
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    try:
        teamName = bs.find('div', class_='ms-entity-header_start').find('a',
                                                                        class_='ms-driver-header_team-title ms-link').text
        driverNumber = bs.find('div', class_='ms-driver_number ms-mr').text
    except AttributeError:
        # TODO пропиши поиск команды и номера по другим ресурсам (напр., википедия),
        # а если сейчас он нигде не числится,
        # то впиши бывший номер и команду с соответствующей припиской, а то не красиво как-то(
        teamName = "Нет команды"
        driverNumber = "(Нет номера)"
    driverName = bs.find('div', class_='ms-entity-header_start').find('h1', class_='ms-entity-header_title').text
    driverAgeData = bs.find('div', class_='ms-entity-header_start').find('span',
                                                                         class_='ms-entity-header_age').text.split()
    driverAgeData = [int("".join(driverAgeData[-1].split(')'))), list(map(int, driverAgeData[0].split('-')))]
    driverNationality = bs.find('img', class_='ms-entity-header_flag').get('title').lower()
    # TODO фотки бери из https://www.skysports.com/f1/drivers-teams,
    # тут они более стандартизированные
    driverPhoto = bs.find('img', class_="ms-item_img ms-item_img--3_2").get('src')
    if not os.path.exists('driverPics/'):
        os.mkdir('driverPics/')
    imageData = requests.get(driverPhoto, verify=False).content
    with open('driverPics/' + driverName + '.jpg', 'wb') as handler:
        handler.write(imageData)
    info = (f"<b>{driverName} №{driverNumber}\n\n</b>"
            f"<b>Команда:</b> {teamName}\n"
            f"<b>Возраст:</b> {driverAgeData[0]}\n"
            f"<b>Дата рождения:</b> {driverAgeData[1][2]}.{driverAgeData[1][1]}.{driverAgeData[1][0]}\n"
            f"<b>Национальность:</b> {translator.translate(driverNationality, dest='ru').text.capitalize()} {flagsEmoji.get(driverNationality)}\n")
    return [info, driverName]

# getDriverInfo('https://ru.motorsport.com/driver/niko-khyulkenberg/63697/')
