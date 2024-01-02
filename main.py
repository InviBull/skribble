from dotenv import load_dotenv

from db.models import User
load_dotenv()

from flask import Flask
from flask_login import (
        LoginManager
)

from utils.env import env
from db.db import create_tables, query 
from routes.auth import auth
from routes.landing import landing

create_tables()

app = Flask(__name__, template_folder='templates')
app.secret_key = env("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    u = query("SELECT * FROM users where id = ?", (userid,))[0]
    try:
        user = User(id=u[0], email=u[1], name=u[2], avatar=[3])
        return user
    except IndexError:
        return User(None)

@app.route('/health')
def health():
    return 'OK'

app.register_blueprint(auth)
app.register_blueprint(landing)

if __name__ == "__main__":
    app.run(port=8000, host='localhost')


