from flask import Blueprint, render_template

landing = Blueprint('landing', __name__, template_folder='templates')

@landing.route
def landingPage():
    return render_template('index.html')
