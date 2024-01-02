from flask import Blueprint, redirect, request
from flask_login import login_required

from db.db import add_notebook, delete_notebook

notebooks = Blueprint('notebooks', __name__, template_folder='templates')

@notebooks.route('/notebooks/add', methods=['POST'])
@login_required
def create_notebook():
    current_user = request.user
    notebook_id = request.form.get("notebook_id")
    notebook_name = request.form.get("notebook_name")
    add_notebook(current_user.id, notebook_id, notebook_name)
    return redirect(f"/{notebook_id}")

@notebooks.route('/notebooks/delete', methods=['POST'])
@login_required
def remove_notebook():
    current_user = request.user
    notebook_id = request.form.get("notebook_id")
    delete_notebook(current_user.id, notebook_id)
    return redirect("/")
