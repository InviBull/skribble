from flask import Blueprint, redirect, request, render_template
from flask_login import login_required, current_user
from uuid import uuid4

from db.db import *

pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route('/<notebook_id>/notes', methods=['POST'])
@login_required
def create_note(notebook_id):
    note_name = request.form.get("note_name")
    note_id = str(uuid4())
    add_note(current_user.id, notebook_id, note_id, note_name, "")
    return redirect(f"/{notebook_id}?noteid={note_id}")

@pages.route('/notebooks/note/delete', methods=['POST'])
@login_required
def remove_note():
    notebook_id = request.form.get("notebook_id")
    note_id = request.form.get("note_id")
    delete_note(current_user.id, notebook_id, note_id)
    return redirect(f"/{notebook_id}")

@pages.route('/notebooks/note/edit', methods=['PUT'])
@login_required
def update_note():
    notebook_id = request.form.get("notebook_id")
    note_id = request.form.get("note_id")
    note_content = request.form.get("note_content")
    edit_note(current_user.id, notebook_id, note_id, note_content)
    return "OK"


@pages.route('/notebooks/note/editTitle', methods=['PUT'])
@login_required
def update_noteTitle():
    print('update title req')
    notebook_id = request.form.get("notebook_id")
    note_id = request.form.get("note_id")
    note_content = request.form.get("new_title")
    edit_note_title(current_user.id, notebook_id, note_id, note_content)
    return "OK"



















































































































































































































