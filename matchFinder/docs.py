import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for)

from matchFinder.db import get_db


bp = Blueprint('docs', __name__, url_prefix='/docs')


@bp.route('/')
def docs():
	return render_template('docs.html')