from http import HTTPStatus

from flask import flash, redirect, render_template, abort

from . import app
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = URLMap.add_link(
        form.original_link.data,
        form.custom_id.data
    )
    if not short:
        flash(f'Имя {form.custom_id.data} уже занято!')
        return render_template('index.html', form=form)
    return (
        render_template(
            'index.html',
            form=form,
            short=short
        ),
        HTTPStatus.OK
    )


@app.route('/<string:short>')
def redirect_view(short):
    original_url = URLMap.get_link(short)
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
