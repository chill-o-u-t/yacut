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
        raise APIError('Отсутствует оригинальная ссылка')
    short = data.get('short_link')
    if short:
        if len(short) > 6 or not re.match(REGEX_PATTERN, short):
            raise APIError('Недопустимая длина ссылки')
        if URLMap.query.filter_by(short=short).first():
            raise APIError(
                'Которткая ссылка {link} уже занята'.format(link=short)
            )
    else:
        short = create_short_url()
    url = URLMap(
        original=data.get('url'),
        short=short
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict(), HTTPStatus.CREATED)


@app.route('api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    original = URLMap.query.filter_by(short=short).first()
    if not original:
        raise APIError('Неизвестная короткая ссылка')
    return jsonify({'url': original.original}, HTTPStatus.OK)
