import logging

def configured_logger(logger):

    logger.setLevel(logging.DEBUG)

    # обработчик для консольного вывода 
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    # обработчик для файлового вывода 
    f_handler = logging.FileHandler('file.log')
    f_handler.setLevel(logging.INFO)

    # форматирование вывода
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('\n'+'---------'*10+'\n'+'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
