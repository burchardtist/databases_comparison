import logging
import os


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    path = os.path.join(os.getcwd(), 'logs')
    filename = '{}.log'.format(name)

    if not os.path.isdir(path):
        os.mkdir(path)

    if not logger.handlers:
        file_handler = logging.FileHandler(
            filename=os.path.join(path, filename),
            mode='a'
        )

        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
