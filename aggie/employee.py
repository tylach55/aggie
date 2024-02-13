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
		'SELECT h.bushells_left, crop, picked, id'
		' FROM harvest h'
		' ORDER BY picked ASC'
	).fetchall()
	return render_template('employee/harvests.html', harvests = harvests)

def get_harvest(id):
	db = get_db()
	harvest = db.execute(
		'SELECT h.bushells_left, picked, crop'
		' FROM harvest h'
		' WHERE h.id=?',(id,)
	).fetchone()
	if harvest is None:
		abort(404, f"harvest id {id} not found")
	return harvest

#create harvests
@bp.route('/create_harvests', methods = ('GET','POST'))
def create_harvests():
	if request.method == 'POST':
		crop = request.form['crop']
		bushells_left = request.form['bushells_left']
		picked =request.form['picked']
		error = None

		if not crop:
			error = "Pick A Crop"
		if not bushells_left:
			error = "How Many Bushells Did You Harvest"
		if not picked:
			error = "USDA requires that you list the date the crop was harested"

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				"INSERT INTO harvest (bushells_left, crop, picked)" "VALUES (?,?,?)",
				(bushells_left, crop, picked)
			)
			db.commit()
			return redirect(url_for("employee.harvests"))

	return render_template('employee/create_harvests.html')


#update harvests
@bp.route('/<int:id>/update_harvest', methods = ("GET", "POST"))
def update_harvests(id, bushells_left=0):
	harvest = get_harvest(id)
	db = get_db()
	if bushells_left > 0:
		db.execute(
			"UPDATE harvest SET bushells_left=? WHERE id=?",(bushells_left, id)
		)
		db.commit()
	return



#delete harvests
@bp.route('/<int:id>/delete_harvests', methods = ("POST",))
def delete_harvests(id):
	harvest = get_harvest(id)
	db = get_db()
	db.execute(
		"DELETE FROM harvest WHERE id = ?", (id,)
	)
	db.commit()
	return 

@bp.route('/shipments')
def shipments():
	db = get_db()
	shipments = db.execute(
		'SELECT s.bushells_of_wheat, bushells_of_walnuts, bushells_of_almonds, id'
		' FROM shipment s'
		' ORDER BY id ASC'
	).fetchall()
	return render_template('employee/shipments.html', shipments = shipments)


def remove_crops_from_harvests(bushells_shipped, crop_shipped):
	if bushells_shipped > 0:
		db = get_db()
		#get all the wheat shipments ordered by picked asc
		#remove the wheat from them
		harvests = db.execute(
			'SELECT h.bushells_left, picked, id'
			' FROM harvest h'
			' WHERE h.crop=?'
			' ORDER BY picked ASC',(crop_shipped,)
		).fetchall()
		for harvest in harvests:
			bushells_in_harvest = int(harvest['bushells_left']) - bushells_shipped
			bushells_shipped -= int(harvest['bushells_left'])
			if bushells_in_harvest <= 0:
				delete_harvests(harvest['id'])
			else:
				update_harvests(harvest['id'], bushells_in_harvest)
			if bushells_shipped <= 0:
				break
		return

	return


def get_shipment(id):
	db = get_db()
	shipment = db.execute(
		'SELECT s.bushells_of_wheat, bushells_of_almonds, bushells_of_walnuts'
		' FROM shipment s'
		' WHERE s.id=?',(id,)
	).fetchone()
	if shipment is None:
		abort(404, f"shipment id {id} not found")
	return shipment

@bp.route('/create_shipments', methods = ('GET','POST'))
def create_shipments():
	if request.method == 'POST':
		bushells_of_wheat = int(request.form['bushells_of_wheat'])
		bushells_of_almonds = int(request.form['bushells_of_almonds'])
		bushells_of_walnuts = int(request.form['bushells_of_walnuts'])
		error = None
		if not bushells_of_walnuts and not bushells_of_almonds and not bushells_of_wheat:
			error = "please pick what to ship"
		#invokes update_harvest
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				"INSERT INTO shipment (bushells_of_wheat, bushells_of_walnuts, bushells_of_almonds)" "VALUES (?,?,?)",
				(bushells_of_wheat, bushells_of_walnuts, bushells_of_almonds)
			)
			db.commit()
			remove_crops_from_harvests(bushells_of_almonds, "almond")
			remove_crops_from_harvests(bushells_of_wheat, "wheat")
			remove_crops_from_harvests(bushells_of_walnuts, "walnut")
			return redirect(url_for("employee.shipments"))

	return render_template('employee/create_shipments.html')

@bp.route('/<int:id>/delete_shipments', methods = ("POST",))
def delete_shipments(id):
	shipments = get_shipment(id)
	db = get_db()
	db.execute(
		"DELETE FROM shipment WHERE id = ?", (id,)
	)
	db.commit()
	return redirect(url_for('employee.shipments'))




