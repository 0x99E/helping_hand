from pydoc import describe
from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify

import models

from . import tools
from . import task_handler
 
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
    uuid = request.args.get('uuid', None, type=str)
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

@blueprint.route('/search_task', methods=['GET', 'POST'])
def search_task():
    per_page = 10

    query = request.form
    
    parameters = None
    if request.is_json:
        parameters = request.json
        query = parameters
    
    response = {"ok": False}
    try:
        tasks = task_handler.search_task(parameters=query)


        for key in tasks:
            response[key] = tasks[key]
        response["ok"] = True
            
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/create_task', methods=['POST'])
def create_task():
    parameters = None
    
    if request.is_json:
        raw_parameters = request.json
        parameters = raw_parameters

    response = {"ok": False}
    try:
        pass
        new_task = task_handler.create_task(parameters)
        if new_task:
            response["ok"] = True
            response["task"] = new_task.to_dict()
            
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/delete_task', methods=['POST'])
def delete_task():
    parameters = None
    
    if request.is_json:
        raw_parameters = request.json
        parameters = raw_parameters

    response = {"ok": True}
    try:
        new_task = task_handler.delete_task(parameters)
            
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/close_task', methods=['POST'])
def close_task():
    parameters = None
    
    if request.is_json:
        raw_parameters = request.json
        parameters = raw_parameters

    response = {"ok": False}
    try:
        task = task_handler.close_task(parameters)
        if task:
            response["task"] = task.to_dict()

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/edit_task', methods=['POST'])
def edit_task():
    parameters = None
    
    if request.is_json:
        raw_parameters = request.json
        parameters = raw_parameters

    response = {"ok": False}
    try:
        task = task_handler.edit_task(parameters)
        if task:
            response["task"] = task.to_dict()
            response = {"ok": True}

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
