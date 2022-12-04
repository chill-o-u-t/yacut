from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from settings import REGEX_PATTERN


class UrlForm(FlaskForm):
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL()
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(6, 16),
            Regexp(REGEX_PATTERN),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
