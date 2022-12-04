from http import HTTPStatus

from flask import flash, redirect, render_template, abort

from . import app, db
from .forms import UrlForm
from .models import URLMap
from .utils import create_short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!')
            return render_template('index.html', form=form)
        if not short:
            short = create_short_url()
        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return (
            render_template(
                'index.html',
                form=form,
                short=short
            ),
            HTTPStatus.OK
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    original_url = URLMap.query.filter_by(short=short).first_or_404()
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
