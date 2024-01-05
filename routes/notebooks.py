from flask import Blueprint, redirect, request
from flask_login import login_required, current_user
from uuid import uuid4

from db.db import add_notebook, delete_notebook, get_notebooks

notebooks = Blueprint('notebooks', __name__, template_folder='templates')

@notebooks.route('/notebooks', methods=['POST'])
@login_required
def create_notebook():
    notebook_name = request.form.get("notebook_name")
    notebook_id = str(uuid4())
    add_notebook(current_user.id, notebook_id, notebook_name)
    return redirect(f"/{notebook_id}")

@notebooks.route('/notebooks', methods=['DELETE'])
@login_required
def remove_notebook():
    notebook_id = request.form.get("notebook_id")
    delete_notebook(current_user.id, notebook_id)
    return redirect("/")

@notebooks.route('/notebooks')
@login_required
def retrieve_notebooks():
    return get_notebooks(current_user.id)
