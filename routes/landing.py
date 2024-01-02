from flask import Blueprint, render_template
from flask_login import current_user

landing = Blueprint('landing', __name__, template_folder='templates')

@landing.route('/')
def landingPage():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return ('<a href="/auth/login">Login</a>')
