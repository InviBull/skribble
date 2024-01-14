from flask import Blueprint, redirect, request, render_template
from flask_login import login_required, current_user
from uuid import uuid4

from db.db import add_note, delete_note, get_notes, get_note

notes = Blueprint('notes', __name__, template_folder='templates')

@notes.route('/<notebook_id>/notes', methods=['POST'])
@login_required
def create_note():
    note_name = request.form.get("note_name")
    notebook_id = request.form.get("notebook_id")
    note_id = str(uuid4())
    add_note(current_user.id, notebook_id, note_id, note_name)
    return redirect(f"/{notebook_id}")

@notes.route('/<notebook_id>/notes', methods=['DELETE'])
@login_required
def remove_note(notebook_id):
    notebook_id = request.form.get("notebook_id")
    note_id = request.form.get("note_id")
    delete_note(current_user.id, notebook_id, note_id)
    return redirect(f"/{notebook_id}")

@notes.route('/<notebook_id>/notes')
@login_required
def retrieve_notes(notebook_id):
    notebook_id = request.args.get("notebook_id")
    return get_notes(current_user.id, notebook_id)
