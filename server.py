from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import rideshares
from flask_app.controllers import messages

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='5150')