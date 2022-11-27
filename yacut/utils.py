import string
from random import choice

from .models import URLMap


def create_short_url():
    short_url = ''.join(
        choice(
            string.ascii_letters + string.digits
        ) for _ in range(6)
    )
    if URLMap.query.filter_by(short=short_url).first():
        return create_short_url()
    return short_url

