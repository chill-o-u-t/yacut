from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from settings import REGEX_PATTERN


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL(message='Введите ссылку целиком')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=16,
                message=f'Длина ссылки должна быть до {16} символов'
            ),
            Regexp(
                REGEX_PATTERN,
                message='Можно использовать только латинские буквы и арабские цифры'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
