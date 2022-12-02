import re

from http import HTTPStatus
from flask import jsonify, request

from settings import REGEX_PATTERN
from . import app, db
from .error_handlers import APIError
from .models import URLMap
from .utils import create_short_url


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if not data:
        raise APIError('Отсутствует тело запроса')
    if not data.get('url'):
        raise APIError('"url" является обязательным полем!')
    short = data.get('custom_id')
    if short:
        if len(short) > 16 or not re.match(REGEX_PATTERN, short):
            raise APIError('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=short).first():
            raise APIError(
                'Имя "{link}" уже занято.'.format(link=short)
            )
    else:
        short = create_short_url()
    url = URLMap(
        original=data.get('url'),
        short=short
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    original = URLMap.query.filter_by(short=short).first()
    if not original:
        raise APIError('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': original.original}), HTTPStatus.OK
