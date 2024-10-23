from flask_app import app   
from flask import redirect, request, session, url_for
from flask_app.models.message import Message

@app.route('/messages/create', methods=['POST'])
def create_message():
    Message.create(request.form)
    rideshare_id = request.form['rideshare_id']
    return redirect(f'/rides/{rideshare_id}')
