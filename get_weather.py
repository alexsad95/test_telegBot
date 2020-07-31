import re
import time
import datetime

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('bot_api.get_weather')


def get_30_day_forecast_content(html):
    '''Собирает данные с сервиса ЯндексПогода, там есть прогноз на 30 дней'''
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.findAll('div', class_='climate-calendar__row')
    rows.pop(0)
    finded_info = []
    for row in rows:
        cells = row.findAll('div', class_='climate-calendar__cell')
        for cell in cells:
            date = cell.find('h6', class_='climate-calendar-day__detailed-day').string.lower()
            temp = cell.find('div', class_='temp climate-calendar-day__detailed-basic-temp-day').span.string
            pressure = int(
                re.findall(r'\d+', 
                    cell.find('table', class_='climate-calendar-day__detailed-data-table').tr.findAll('td')[1].string
                )[0])
            humidity = cell.find('table', class_='climate-calendar-day__detailed-data-table').tr.findAll('td')[3].string
            finded_info.append({
                'date': date, 
                'temp': temp, 
                'pressure': pressure, 
                'humidity': humidity
                })
    return finded_info


def get_our_item(finded_info, date_for_search):
    '''Берёт с прогноза погоды необходимую дату'''
    try:
        date_for_search = datetime.datetime.fromisoformat(date_for_search)
        current_date = date_for_search.strftime("%d %B, %a").lower()
        our_finded_item = None
        for item in finded_info:
            date = datetime.datetime.strptime(item['date'] + ", " + str(datetime.datetime.now().year), "%d %B, %a, %Y")
            date = date.strftime("%d %B, %a").lower()
            if date == current_date:
                our_finded_item = item
                return our_finded_item
        if not our_finded_item:
            logging.warning('Не была найдена погода. our_finded_item: %s', our_finded_item)
    except ValueError as e:
        logger.warning(e, exc_info=True)
        logger.info('date_for_search: ' + str(date_for_search))
    except Exception as e:
        logger.error(e, exc_info=True)


def get_weather_info(place, date_for_search):
    try:
        '''Основная фун-ия, вызывает остальные, парсит и возвращает данные по погоде'''
        response = requests.get('https://yandex.md/weather/search?request='+place).text
        soup = BeautifulSoup(response, 'html.parser')

        a_href = soup.find('div', class_='place-list place-list_ancient-design_yes').li.a.get('href')
        url = 'https://yandex.md'+a_href[:-8]+'/month'
        html = requests.get(url).text
        items = get_30_day_forecast_content(html)
        finded_item = get_our_item(items, date_for_search)
        return finded_item

    except Exception as e:
        logger.error(e, exc_info=True)