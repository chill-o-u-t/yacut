from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app, db
from .forms import UrlForm
from .models import URLMap
from .utils import create_short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short = form.short.data
        if not short:
            short = create_short_url()
        if URLMap.query.filter_by(short=short).first():
            flash('Такая короткая ссылка уже есть!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=form.original.data,
            short=form.short.data
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
def redirect_short(short):
    original = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(original.original)