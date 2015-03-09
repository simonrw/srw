import logging


logging.basicConfig(
    level='DEBUG', format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')


def get_logger(*args, **kwargs):
    return logging.getLogger(*args, **kwargs)
