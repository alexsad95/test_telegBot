import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

import config
from get_weather import get_weather_info
from vk_api_async import do_all_this_proccess
from log import configured_logger

logger = logging.getLogger('bot_api')
logger = configured_logger(logger)

API_TOKEN = config.TOKEN_BOT

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='vk_api')
async def get_vk_group_articles(message):
    command = message.text.split()[1:]

    if len(command) == 0:
        await message.answer('Введите домен группы')
        return

    group = command[0]
    
    await dp.loop.create_task(do_all_this_proccess(group))
    file = InputFile('articles.csv')
    await message.answer_document(file)


@dp.message_handler(commands=['help'])
async def do_help_command(message):
    help_message = 'Как работает бот.\n \
/help - инфо по боту\n \
/weather Москва 2020-07-24 - запрашивает прогноз погоды на указанный город и дату\n\
/vk_api yvkurse - собирает статьи с группы'
    await message.answer(help_message)


@dp.message_handler(commands=['weather'])
async def get_weather_forcast(message):
    command = message.text.split()[1:]

    if len(command) != 2:
        await message.answer('Не правильно введены параметры')
        return

    place = command[0]
    date_for_search = command[1]

    finded_item = get_weather_info(place, date_for_search)
    if not finded_item:
        output_message = 'Не правильно введена дата, или что-то не то'
        logger.error('Find_item is None')
    else:
        output_message = f"В городе {place} на {date_for_search}: \n\
- температура {finded_item['temp']}°С \n\
- давление {finded_item['pressure']} мм рт.ст \n\
- влажность {finded_item['humidity']}"

    await message.answer(output_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
