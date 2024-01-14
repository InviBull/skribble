from flask import Blueprint, redirect, request, render_template
from flask_login import login_required, current_user
from uuid import uuid4

from db.db import *

notebooks = Blueprint('notebooks', __name__, template_folder='templates')

@notebooks.route('/notebooks', methods=['POST'])
@login_required
def create_notebook():
    notebook_name = request.form.get("notebook_name")
    notebook_id = str(uuid4())
    add_notebook(current_user.id, notebook_id, notebook_name)
    return redirect(f"/{notebook_id}")

@notebooks.route('/notebooks/delete', methods=['POST'])
@login_required
def remove_notebook():
    notebook_id = request.form.get("notebook_id")
    delete_notebook(current_user.id, notebook_id)
    return redirect("/")

@notebooks.route('/notebooks')
@login_required
def retrieve_notebooks():
    return get_notebooks(current_user.id)

@notebooks.route('/<notebook_id>')
@login_required
def retrieve_notebook(notebook_id):
    notebook = get_notebook(current_user.id, notebook_id)
    if len(notebook) == 0:
        return '<p>Notebook not found</p>'

    notebook = notebook[0]
    if notebook[0] != current_user.id:
        return '<p>Unauthorized</p>'

    notes = get_notes(current_user.id, notebook_id)

    return render_template('notes.html', name=current_user.name, notebook_id=notebook_id, notebook=notebook, notes=notes)

@notebooks.route('/<notebook_id>/notes', methods=['POST'])
@login_required
def create_note(notebook_id):
    note_name = request.form.get("note_name")
    note_id = str(uuid4())
    add_note(current_user.id, notebook_id, note_id, note_name, "")
    return redirect(f"/{notebook_id}")









