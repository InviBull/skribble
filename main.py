from dotenv import load_dotenv
load_dotenv()

from flask import Flask
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
    u = query("SELECT * FROM users where id = ?", (userid))
    try:
        return u[0]
    except IndexError:
        return None

@app.route('/health')
def health():
    return 'OK'

app.register_blueprint(auth)
app.register_blueprint(landing)
app.register_blueprint(notebooks)

if __name__ == "__main__":
    app.run(port=8000, host='localhost')


