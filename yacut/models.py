import re
from datetime import datetime
from random import choice

from flask import url_for

from settings import (
    MAX_LINK_LENGTH,
    MAX_LOOP_COUNT,
    EMPTY_ORIGINAL_LINK,
    REGEX_PATTERN,
    WRONG_SHORT_LINK,
    LINK_IS_IN_DB,
    LETTERS_FOR_SHORT_LINK,
    AUTOGENERATED_LENGTH,
)
from yacut import db


class URLMap(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(),
        nullable=False,
        index=True
    )
    short = db.Column(
        db.String(MAX_LINK_LENGTH),
        index=True,
        unique=True
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    @staticmethod
    def check_api_short(original, short):
        if not original:
            return EMPTY_ORIGINAL_LINK
        if short:
            if (
                len(short) > MAX_LINK_LENGTH or not
                re.match(REGEX_PATTERN, short)
            ):
                return WRONG_SHORT_LINK
            if URLMap.query.filter_by(short=short).first():
                return LINK_IS_IN_DB.format(link=short)

    @staticmethod
    def create_short_url():
        for _ in range(MAX_LOOP_COUNT):
            short_url = ''.join(
                choice(
                    LETTERS_FOR_SHORT_LINK
                ) for _ in range(AUTOGENERATED_LENGTH)
            )
            if not URLMap.query.filter_by(short=short_url).first():
                return short_url

    @staticmethod
    def add_link(original, short):
        if URLMap.query.filter_by(short=short).first():
            return
        if not short:
            short = URLMap.create_short_url()
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return short

    @staticmethod
    def get_link(short):
        return (
            URLMap.query.filter_by(
                short=short
            ).first()
        )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view',
                short=self.short,
                _external=True
            )
        )
