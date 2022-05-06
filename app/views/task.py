
from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify

import models
import handlers
 
blueprint = Blueprint('task', __name__, url_prefix='/task')


@blueprint.route('/get_task', methods=['GET'])
def get_task():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        response = handlers.TASK.get_task(parameters)

    except:
        pass
    return jsonify(response)


@blueprint.route('/get_tasks', methods=['GET'])
def get_tasks():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.TASK.get_tasks(parameters)

    except:
        pass

    return jsonify(response)


@blueprint.route('/get_last', methods=['GET'])
def get_last():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        response = handlers.TASK.get_last(parameters)

    except:
        pass
    return jsonify(response)


@blueprint.route('/create_task', methods=['POST'])
def create_task():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        raw_response = handlers.TASK.create_task(parameters)
        response = handlers.TASK.create_view(raw_response, "task")
            
    except:
        pass
    return jsonify(response)


@blueprint.route('/edit_task', methods=['POST'])
def edit_task():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:

        raw_response = handlers.TASK.edit_task(parameters)
        response = handlers.TASK.create_view(raw_response, "task")

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)


@blueprint.route('/close_task', methods=['POST'])
def close_task():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        raw_response = handlers.TASK.close_task(parameters)
        response = handlers.TASK.create_view(raw_response, "task")

    except:
        pass
    return jsonify(response)


@blueprint.route('/delete_task', methods=['POST'])
def delete_task():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.TASK.delete_task(parameters)
            
    except:
        pass
    return jsonify(response)


# @blueprint.route('/statistics', methods=['GET'])
# def statistics():
#     response = {"ok": False}
#     try:
#         total_open = models.Task.query.filter_by(closed=False).count()
#         total_closed = models.Task.query.filter_by(closed=True).count()
#         total_user = total_open + total_closed
#         response["ok"] = True
#         response["open"] = total_open
#         response["closed"] = total_closed
#         response["total"] = total_user

#     except Exception as e:
#         response["error"] = str(e)
#     return jsonify(response)
