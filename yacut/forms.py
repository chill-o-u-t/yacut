from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class UrlForm(FlaskForm):
    original = URLField(
        'Введите оригинальную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 128),
            URL()
        ]
    )
    short = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(6, 6), Optional()]
    )
    submit = SubmitField('Создать')
