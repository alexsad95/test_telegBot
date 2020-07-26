import re
import time
import datetime

import requests
from bs4 import BeautifulSoup


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
    date_for_search = datetime.datetime.fromisoformat(date_for_search)
    current_date = date_for_search.strftime("%d %B, %a").lower()
    our_finded_item = None
    for item in finded_info:
        if item['date'] == current_date:
            our_finded_item = item
    return our_finded_item

def get_weather_info(place, date_for_search):
    '''Основная фун-ия, вызывает остальные, парсит и возвращает данные по погоде'''
    response = requests.get('https://yandex.md/weather/search?request='+place).text
    soup = BeautifulSoup(response, 'html.parser')

    a_href = soup.find('div', class_='place-list place-list_ancient-design_yes').li.a.get('href')
    url = 'https://yandex.md'+a_href[:-8]+'/month'
    
    html = requests.get(url).text
    items = get_30_day_forecast_content(html)
    finded_item = get_our_item(items, date_for_search)

    return finded_item
