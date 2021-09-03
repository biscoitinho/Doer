from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Ttable, Task
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import session
from . import db
import sys

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
    if "_" in tablename:
      tabname = tablename.replace("_", " ")
    else:
      tabname = tablename

    get_table = Ttable.query.filter(tabname == Ttable.name).first()
    if tabname in str(get_table):
      flash("Table with this name already exists")
      return redirect(url_for('main.tables'))
    else:
      new_table = Ttable(name = tabname, email = current_user.email)

      db.session.add(new_table)
      db.session.commit()

      return redirect(url_for('main.tables'))

@main.route('/tables/<tablename>/<id>/edit', methods=['GET'])
@login_required
def edit_table_form(tablename, id):
    return render_template('edit_table.html', tablename = tablename.replace(" ", "_"), id = id)

@main.route('/tables/<tablename>/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_table(tablename, id):
    new_tablename = request.form.get('name')
    if "_" in new_tablename:
      tabname = new_tablename.replace("_", " ")
    else:
      tabname = new_tablename

    get_table = Ttable.query.filter(tabname == Ttable.name).first()
    if tabname in str(get_table):
      flash("Table with this name already exists")
      return redirect(url_for('main.tables'))

    edit = db.session.query(Ttable).filter(Ttable.name == tablename.replace("_", " ")).filter(Ttable.id == id).first()
    if tabname:
      edit.name = tabname
      db.session.commit()

      return redirect(url_for('main.tables'))

@main.route('/tables/<tablename>/<id>/delete', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_table(tablename, id):
    query = Ttable.query.all()
    get_table = Ttable.query.filter(id == Ttable.id).first()
    if not get_table:
        return render_template("tables.html", ttable = query, name = current_user.name)

    #Delete all the tasks to the corresponding table
    db.session.query(Task).filter(Task.ttable_id == id).delete()
    db.session.delete(get_table)
    db.session.commit()
    flash("Table deleted")
    return render_template("index.html")

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
    return render_template("tasks.html", tablename = tablename, query = query)

@main.route('/tables/<tablename>/kanban', methods=["GET"])
@login_required
def kanban(tablename):
    query = db.session.query(
                            Task.id, Task.name,
                            Task.description,
                            Task.status,
                            Task.ttable_id,
                            Ttable.email,
                            ).join(
                                  Ttable,
                                  Ttable.id == Task.ttable_id).filter(Ttable.name == tablename.replace("_", " "))
    return render_template("kanban.html", tablename = tablename, query = query)

@main.route('/tables/<tablename>/task/create')
@login_required
def new_task(tablename):
    return render_template("new_task.html", tablename = tablename)

@main.route('/tables/<tablename>/task/create', methods=['GET', 'POST'])
@login_required
def create_task(tablename):
    query = Ttable.query.all()
    name = request.form.get('name')
    description = request.form.get('description')
    # SCALAR - Return the first element of the first result or None if no rows present.
    # If multiple rows are returned, raises MultipleResultsFound.
    tid = db.session.query(Ttable.id).filter(Ttable.name == tablename.replace("_", " ")).scalar()
    status = request.form.get('status')
    new_task = Task(name = name, description = description, ttable_id = tid, status = status)

    db.session.add(new_task)
    db.session.commit()

    return render_template("tables.html", ttable = query, name = current_user.name)

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

@main.route('/tables/<tablename>/task/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(tablename, id):
    new_name = request.form.get('name')
    new_description = request.form.get('description')
    new_status = request.form.get('status')
    edit = Task.query.filter(id == Task.id).first()
    if new_name:
        edit.name = new_name
    if new_description:
        edit.description = new_description
    if new_status:
        edit.status = new_status

    db.session.commit()

    #return render_template("tasks.html", tablename = tablename, query = query)
    if request.method == "GET":
        return render_template('edit_task.html', tablename = tablename, id = id, description = edit.description, name = edit.name)
    if request.method == "POST":
        return redirect(url_for('main.tables'))

@main.route('/tables/<tablename>/task/<id>/delete', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_task(tablename, id):
    query = Ttable.query.all()
    get_task = Task.query.filter(id == Task.id).first()
    if not get_task:
        return render_template("tables.html", ttable = query, name = current_user.name)

    db.session.delete(get_task)
    db.session.commit()
    flash("Task deleted")

    return render_template("tables.html", ttable = query, name = current_user.name)
