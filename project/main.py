from flask import Blueprint, render_template, request, redirect, url_for
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

@main.route('/table')
@login_required
def table():
    return render_template('table.html')

@main.route('/table', methods=['GET', 'POST'])
@login_required
def create_table():
    tablename = request.form.get('tablename')
    new_table = Ttable(name = tablename, email = current_user.email)

    db.session.add(new_table)
    db.session.commit()

    return render_template('index.html')

@main.route('/tables/<tablename>/tasks', methods=["GET"])
@login_required
def tasks(tablename):
    query = db.session.query(
                            Task.id, Task.name,
                            Task.description,
                            Task.status,
                            Task.ttable_id,
                            Ttable.email,
                            ).join(
                                  Ttable,
                                  Ttable.id == Task.ttable_id).filter(Ttable.name == tablename.replace("_", " "))
    print(query)
    return render_template("tasks.html", tablename = tablename, query = query)

@main.route('/tables/<tablename>/task/create')
@login_required
def new_task(tablename):
    return render_template("new_task.html", tablename = tablename)

@main.route('/tables/<tablename>/task/create', methods=['GET', 'POST'])
@login_required
def create_task(tablename):
    name = request.form.get('name')
    description = request.form.get('description')
    tid = db.session.query(Ttable.id).filter(Ttable.name == tablename.replace("_", " "))
    status = request.form['status']
    new_task = Task(name = name, description = description, ttable_id = tid, status = status)

    db.session.add(new_task)
    db.session.commit()

    return render_template('index.html')

@main.route('/tables/<tablename>/task/<id>', methods=["GET", "POST"])
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

@main.route('/tables/<tablename>/task/<id>/delete', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_task(tablename, id):
    query = Ttable.query.all()
    get_task = Task.query.filter(id == Task.id).first()
    if not get_task:
        return render_template("tables.html", ttable = query, name = current_user.name)

    db.session.delete(get_task)
    db.session.commit()
    return render_template("tables.html", ttable = query, name = current_user.name)
