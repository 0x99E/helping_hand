from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify

import models

from . import tools

blueprint = Blueprint('task', __name__, url_prefix='/task')

# Get all users with pagination
@blueprint.route('/get_tasks', methods=['GET'])
def get_tasks():
    per_page = 10
    page = request.args.get('page', 1, type=int)
    response = {"ok": False}
    try:
        total_number = models.Task.query.count()
        raw_tasks = models.Task.query.paginate(page, per_page, False).items
        tasks = []
        for user in raw_tasks:
            tasks.append(user.to_dict())
        response["ok"] = True
        response["tasks"] = tasks
        response["total"] = total_number
        response["current_page"] = page
        response["total_page"] = total_number // per_page + 1

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/get_task', methods=['GET'])
def get_task():
    uuid = request.args.get('uuid', 0, type=str)
    response = {"ok": False}
    try:
        task = models.Task.query.filter_by(uuid=uuid).first()
        if task == None:
            task = []
        else:
            task = task.to_dict()
        response["ok"] = True
        response["task"] = task
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/create_task', methods=['GET'])
def create_task():
    name = request.args.get('name', "", type=str)
    description = request.args.get('description', "", type=str)
    student = request.args.get('student', "", type=str)
    mentor = request.args.get('mentor', "", type=str)

    response = {"ok": False}
    try:
        user_exists = bool(models.User.query.filter_by(uuid=student).first())
        if user_exists:
            pass
            if name == "":
                raise Exception("Name is required!")
            task_exist = True
            while task_exist:
                uuid = "task_" + tools.random_string(20)
                task_exist = bool(models.Task.query.filter_by(uuid=uuid).first())
            
            temp_task = models.Task(name=name, description=description, student=student, mentor=mentor, uuid=uuid)
            models.db.session.add(temp_task)
            models.db.session.commit()
            response["ok"] = True
            response["task"] = temp_task.to_dict()

        else:
            raise Exception("User uuid not exist!")
            
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/statistics', methods=['GET'])
def statistics():
    response = {"ok": False}
    try:
        total_open = models.Task.query.filter_by(closed=False).count()
        total_closed = models.Task.query.filter_by(closed=True).count()
        total_user = total_open + total_closed
        response["ok"] = True
        response["open"] = total_open
        response["closed"] = total_closed
        response["total"] = total_user

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
