from http import HTTPStatus
from flask import jsonify, request

from . import app
from .error_handlers import APIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if not data:
        raise APIError('Отсутствует тело запроса')
    check = URLMap.check_api_short(
        data.get('url'),
        data.get('custom_id')
    )
    if check:
        raise APIError(check)
    short = URLMap.add_link(
        data.get('url'),
        data.get('custom_id')
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
