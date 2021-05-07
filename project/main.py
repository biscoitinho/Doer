from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User, Ttable, Task
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import session
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name)

@main.route('/tables', methods=["GET", "POST"])
@login_required
def tables():
    query = Ttable.query.all()
    if request.method == "GET":
      return render_template("tables.html", ttable = query, name = current_user.name)

    if not current_user.is_authenticated:
      return redirect(url_for('index'))

@main.route('/<tablename>/tasks', methods=["GET", "POST"])
@login_required
def tasks(tablename):
    query = db.session.query(
                            Task.id, Task.name,
                            Task.description,
                            Task.status,
                            Ttable.email
                            ).join(
                                  Ttable,
                                  Ttable.id == Task.ttable_id)
    return render_template("tasks.html", tablename = tablename, query = query)

@main.route('/<tablename>/<id>', methods=["GET", "POST"])
@login_required
def task(tablename, id):
    query = db.session.query(
                            Task.id, Task.name,
                            Task.description,
                            Task.status,
                            Ttable.email
                            ).join(
                                  Ttable,
                                  Ttable.id == Task.ttable_id).filter(
                                                                      Task.id == id)
    return render_template("task.html", tablename = tablename, id = Task.id, query = query)

@main.route('/<tablename>/<id>/delete', methods=['DELETE'])
@login_required
def delete_task(tablename, id):
    get_task = db.session.query(
                            Task.id,
                            Ttable.email,
                            Ttable.name
                            ).join(
                                  Ttable,
                                  Ttable.id == Task.ttable_id).filter(
                                                                      Task.id == id,
                                                                      Ttable.name == tablename)
    db.session.delete(get_task)
    db.session.commit()
    return "Deleted"
