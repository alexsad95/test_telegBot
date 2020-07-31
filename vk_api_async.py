import csv

import asyncio
import aiohttp
from bs4 import BeautifulSoup

import config


async def get_res(session, url, params):
    '''Делает запрос на сайт и выводит данные. В основном json. Если не он, то текст'''
    async with session.get(url, params=params) as resp:
        try: 
            result = await resp.json()
        except:
            result = await resp.text()
        return result


def get_article(data):
    '''Отбирает статьи из данных по запросам к VK API'''
    list_with_data_articles = []
    for post in data:
        items = post['response']['items']
        for item in items:
            try:
                if (item['attachments'][0]['link']) and (item['attachments'][0]['link']['description'] == 'Article'):
                    title = item['attachments'][0]['link']['title']
                    url = item['attachments'][0]['link']['url'] 
                    sizes = []
                    for size in item['attachments'][0]['link']['photo']['sizes']:
                        sizes.append(size['url'])
                    list_with_data_articles.append([ 
                        title, url, sizes[0], 
                        sizes[1], sizes[2], sizes[3], 
                        sizes[4], sizes[5], sizes[6], 
                        sizes[7], sizes[8] 
                    ])
            except:
                pass
    return list_with_data_articles


async def do_all_this_proccess(domain):
    '''Основная фун-ия'''

    params = {
        'access_token': config.VK_KEY_API,
        'v': '5.120',
        'domain': domain,
        'count': 1
    }

    async with aiohttp.ClientSession() as session:
        all_params = []

        # запрос чтобы узнать количество постов
        result = await get_res(session, 'https://api.vk.com/method/wall.get', params)
        count = result['response']['count']

        params['count'] = 100
        params['offset'] = 0

        # запросы по всем постам
        while params['offset'] < count:
            all_params.append(params.copy())
            params['offset'] += 100

        # выполняет асинхронно все таски с запросами 
        tasks = [get_res(session, 'https://api.vk.com/method/wall.get', iter_param) for iter_param in all_params]
        results = await asyncio.gather(*tasks)

        # сбор всех статей с постов
        articles = get_article(results)

        # таски для парсинга текста с статьи
        tasks = [get_res(session, article_item[1], None) for article_item in articles]
        results = await asyncio.gather(*tasks)

        # парсинг самого текста с тегов
        copy_results = results[:]
        for i, res in enumerate(copy_results):
            soup = BeautifulSoup(res, 'html.parser')
            body = [p.text for p in soup.find('div', class_='article article_view article_mobile').findAll('p')]
            articles[i].append(body)

        # запись всего в файл csv
        with open('articles.csv', 'w') as file:
            csv_manager = csv.writer(file)
            csv_manager.writerow((
                'title', 'url', 'body', 
                'sizes_m', 'sizes_o', 'sizes_p', 
                'sizes_q', 'sizes_r', 'sizes_s', 
                'sizes_x', 'sizes_y', 'sizes_z'
            ))
            for article_data in articles:
                csv_manager.writerow((
                    article_data[0], article_data[1], article_data[11], 
                    article_data[2], article_data[3], article_data[4], 
                    article_data[5], article_data[6], article_data[7], 
                    article_data[8], article_data[9], article_data[10]
                ))
