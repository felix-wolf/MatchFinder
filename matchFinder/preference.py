import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for)

from matchFinder.db import get_db


bp = Blueprint('preference', __name__, url_prefix='/preference')
