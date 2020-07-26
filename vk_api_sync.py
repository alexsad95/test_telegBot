'''
   По началу написал так, но выполняется долго все примерно 30-40 сек.
   Пришлось распараллелить
'''
import csv 
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import config

def get_all_posts():
    token = config.VK_KEY_API
    version = '5.120'
    domain = 'yvkurse'
    count = 100
    offset = 0
    all_posts = [] 

    count = requests.get('https://api.vk.com/method/wall.get',
            params={
                'access_token': token,
                'v': version,
                'domain': domain,
                'count': 1,
            }
        )
    count = count.json()['response']['count']

    while offset < count:
        response = requests.get('https://api.vk.com/method/wall.get',
            params={
                'access_token': token,
                'v': version,
                'domain': domain,
                'count': count,
                'offset': offset
            }
        )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
    return all_posts

def file_writer(data):
    with open('post_json.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow((
            'title', 'url', 'body', 
            'sizes_m', 'sizes_o', 'sizes_p', 
            'sizes_q', 'sizes_r', 'sizes_s', 
            'sizes_x', 'sizes_y', 'sizes_z'
        ))
        for post in data:
            try:
                if (post['attachments'][0]['link']) and (post['attachments'][0]['link']['description'] == 'Article'):
                    title = post['attachments'][0]['link']['title']
                    url = post['attachments'][0]['link']['url'] 
                    res = requests.get(url).text
                    soup = BeautifulSoup(res, 'html.parser')
                    body = [p.text for p in soup.find('div', class_='article article_view article_mobile').findAll('p')]
                    sizes = []
                    for size in post['attachments'][0]['link']['photo']['sizes']:
                        sizes.append(size['url'])

                a_pen.writerow((
                    title, url, body, 
                    sizes[0], sizes[1], sizes[2], 
                    sizes[3], sizes[4], sizes[5], 
                    sizes[6], sizes[7], sizes[8]
                ))
            except:
                pass

start = datetime.now() 
all_posts = get_all_posts()
point_two = datetime.now()
print(point_two-start)
file_writer(all_posts)
print(datetime.now() - point_two)