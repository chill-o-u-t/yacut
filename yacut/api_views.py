import re

from http import HTTPStatus
from flask import jsonify, request

from settings import REGEX_PATTERN
from . import app, db
from .error_handlers import APIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if not data:
        raise APIError('Отсутствует тело запроса')
    if not data.get('url'):
        raise APIError('"url" является обязательным полем!')
    if (
        len(data.get('custom_id')) > 16
        or not re.match(REGEX_PATTERN, data.get('custom_id'))
    ):
        raise APIError('Указано недопустимое имя для короткой ссылки')
    short = URLMap.add_link(
        data.get('url'),
        data.get('custom_id')
    )
    if not short:
        raise APIError(
            'Имя "{link}" уже занято.'.format(link=short)
        )
    return jsonify(
        URLMap.get_link(short).to_dict()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    original = URLMap.get_link(short)
    if not original:
        raise APIError('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': original.original}), HTTPStatus.OK
