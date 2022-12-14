from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    URL,
    Regexp
)

from settings import PATTERN, MAX_LINK_LENGTH, MAX_URL_LENGTH

SUBMIT_FIELD = 'Создать'
REGEX_FIELD = (
    'Можно использовать только '
    'латинские буквы и арабские цифры'
)
SHORT_LENGTH_FIELD = (
    'Длина ссылки должна быть до '
    '{} символов'
)
SHORT_DESCRIPTION = 'Ваш вариант короткой ссылки'
ORIGINAL_DESCRIPTION = 'Длинная ссылка'
URL_FIELD = 'Введите ссылку целиком'
DATA_REQUIRED_FIELD = 'Обязательное поле'


class UrlForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_DESCRIPTION,
        validators=[
            DataRequired(message=DATA_REQUIRED_FIELD),
            URL(message=URL_FIELD),
            Length(max=MAX_URL_LENGTH)
        ]
    )
    custom_id = StringField(
        SHORT_DESCRIPTION,
        validators=[
            Length(
                max=MAX_LINK_LENGTH,
                message=SHORT_LENGTH_FIELD.format(
                    MAX_LINK_LENGTH
                )
            ),
            Regexp(
                PATTERN,
                message=REGEX_FIELD
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_FIELD)
