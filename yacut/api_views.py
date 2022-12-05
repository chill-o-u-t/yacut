import re

from http import HTTPStatus
from flask import jsonify, request

from settings import REGEX_PATTERN, MAX_LINK_LENGTH
from . import app, db
from .error_handlers import APIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    check = URLMap.check_api_short(data)
    if check:
        raise APIError(check)
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
