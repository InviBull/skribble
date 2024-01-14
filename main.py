from dotenv import load_dotenv
import os

from db.models import User
load_dotenv()

from flask import Flask, url_for
from flask_login import (
        LoginManager
)

from utils.env import env
from db.db import create_tables, query 
from routes.auth import auth
from routes.landing import landing
from routes.notebooks import notebooks

create_tables()

app = Flask(__name__, template_folder='templates')
app.secret_key = env("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        u = query("SELECT * FROM users where id = ?", (userid,))[0]
        user = User(id=u[0], email=u[1], name=u[2], avatar=[3])
        return user
    except IndexError:
        return User(id=None)

@app.route('/health')
def health():
    return 'OK'

app.register_blueprint(auth)
app.register_blueprint(landing)
app.register_blueprint(notebooks)

# Refresh CSS
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(debug=True, port=9989, host='localhost')


