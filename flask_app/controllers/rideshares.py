from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.rideshare import Rideshare
from flask_app.models.message import Message
from pprint import pprint

@app.route('/rides/dashboard')
def display_dashboard():
    # User must be logged in to view page
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login'))
    all_rideshares = Rideshare.get_all()
    return render_template('dashboard.html', rideshares=all_rideshares)

@app.route('/rides/new', methods = ['GET', 'POST'])
def create_rideshare():
    if request.method == 'GET':
        # User must be logged in to view page
        if 'logged_in_user_id' not in session:
            return redirect(url_for('display_reg_login'))
        return render_template('create_rideshare.html')
    elif request.method == 'POST':
        if not Rideshare.validate_rideshare(request.form):
            session['create_rideshare_data'] = request.form
            return redirect(url_for('create_rideshare'))
        # If form passes validation, create rideshare and remove create_rideshare_data from session
        if 'create_rideshare_data' in session:
            session.pop('create_rideshare_data')
        Rideshare.create(request.form)
        return redirect(url_for('display_dashboard'))
    
@app.route('/rides/edit/<int:rideshare_id>', methods=['GET', 'POST'])
def edit_rideshare(rideshare_id):
    if request.method == 'GET':
        # User must be logged in to view page
        if 'logged_in_user_id' not in session:
            return redirect(url_for('display_reg_login'))
        this_rideshare = Rideshare.get_one_by_id_with_rider_and_driver(rideshare_id)
        return render_template('edit_rideshare.html', rideshare=this_rideshare)
    elif request.method == 'POST':
        if not Rideshare.validate_rideshare_edit(request.form):
            return redirect(url_for('create_rideshare'))
        Rideshare.update_rideshare(request.form)
        return redirect(url_for('display_dashboard'))
    
@app.route('/rides/delete/<int:rideshare_id>')
def delete_rideshare(rideshare_id):
    Rideshare.delete(rideshare_id)
    return redirect(url_for('display_dashboard'))

@app.route('/rides/edit_driver', methods=['POST'])
def edit_driver():
    rideshare_id = request.form['rideshare_id']
    driver_id = request.form['driver_id']
    if driver_id == 'None':
        driver_id = None
    Rideshare.update_driver(rideshare_id, driver_id)
    return redirect(url_for('display_dashboard'))

@app.route('/rides/<int:rideshare_id>')
def display_one_rideshare(rideshare_id):
    # User must be logged in to view page
    if 'logged_in_user_id' not in session:
        return redirect(url_for('display_reg_login'))
    one_rideshare = Rideshare.get_one_by_id_with_rider_and_driver(rideshare_id)
    all_messages = Message.get_all()
    return render_template('display_one_rideshare.html', rideshare=one_rideshare, messages=all_messages)