import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JSON_AS_ASCII = False


REGEX_PATTERN = '^[A-Za-z0-9]+$'
MAX_LINK_LENGTH = 16
LETTERS_FOR_SHORT_LINK = string.ascii_letters + string.digits
AUTOGENERATED_LENGTH = 6
MAX_LOOP_COUNT = 16
MAX_URL_LENGTH = 2048

EMPTY_BODY = 'Отсутствует тело запроса'
EMPTY_ORIGINAL_LINK = '"url" является обязательным полем!'
WRONG_SHORT_LINK_REGEX = 'Указано недопустимое имя для короткой ссылки'
WRONG_SHORT_LINK_LEN = 'Указана недопустимая длина ссылка'
LINK_IS_IN_DB = 'Имя "{link}" уже занято.'
