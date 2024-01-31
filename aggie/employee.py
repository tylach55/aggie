from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
#from aggie.auth import login_required
from aggie.db import get_db

bp = Blueprint('employee', __name__, url_prefix='/employee')


#read harvests
@bp.route('/harvests')
def harvests():
	db = get_db()
	harvests = db.execute(
		'SELECT h.bushells_left, crop, expiration, picked'
		' FROM harvest h'
		' ORDER BY picked ASC'
	).fetchall()
	return render_template('employee/harvests.html', harvests = harvests)

"""
#create harvests
@bp.route('/harvests/create_harvest')
def create_harvests():
	return render_template('create_harvests.html')

#update harvests
@bp.route('update_harvest')
def update_harvests():
	return render_template('update_harvests.html')

#delete harvests
@bp.route('delete_harvests')
def delete_harvests():
	return render_template('delete_harvests.html')
	"""


