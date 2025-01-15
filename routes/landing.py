from flask import Blueprint, render_template
from flask_login import current_user

from db.db import get_notebooks

landing = Blueprint('landing', __name__, template_folder='templates')

@landing.route('/')
def landingPage():
    if current_user.is_authenticated:
        notebooks = get_notebooks(current_user.id) 
        print(current_user.get_avatar())
        return render_template('index.html', length=len(notebooks), notebooks=notebooks, user_avatar=current_user.get_avatar())
    else:
        return render_template('landing.html')
