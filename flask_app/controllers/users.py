from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
# from flask_app.models.post import Post
# from flask_app.models.comment import Comment
from pprint import pprint

@app.route('/')
def display_reg_login():
    return render_template('register_login.html')

@app.route('/register', methods=['POST'])
def create_user():
    pprint(request.form)
    if not User.validate_user(request.form):
        session['create_user_data'] = request.form
        return redirect(url_for('display_reg_login'))
    # If form data passes validation, create user
    if 'create_user_data' in session:
        session.pop('create_user_data')
    User.create(request.form)
    # Save user id and name to session for access to site
    new_user = User.get_one_by_email(request.form)
    session['logged_in_user_id'] = new_user.id
    session['logged_in_user_first_name'] = new_user.first_name
    return redirect(url_for('display_dashboard'))

@app.route('/login', methods=['POST'])
def login_user():
    valid_user = User.login(request.form)

    if not valid_user:
        return redirect(url_for('display_reg_login'))
    
    # If validation is successful, user logs in. Save user ID to session
    session['logged_in_user_id'] = valid_user.id
    session['logged_in_user_first_name'] = valid_user.first_name

    print(f'ID: {session['logged_in_user_id']} NAME: {session['logged_in_user_first_name']}')
    return redirect(url_for('display_dashboard'))

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect(url_for('display_reg_login'))