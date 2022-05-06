
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

    query = request.args.get('query', "", type=str)
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', "all", type=str)


        
    mentor = request.args.get('mentor', None, type=str)
    student = request.args.get('student', None, type=str)

    parameters = {
        "sort": sort,
        "mentor": mentor,
        "student": student,
    }

    response = {"ok": False}
    try:
        atasks = task_handler.search_task(query=query, page=page, per_page=per_page, parameters=parameters)
        tasks = atasks['tasks']
        info = atasks['info']

        total_number = info['total']
        response["ok"] = True
        response["tasks"] = tasks
        response["total"] = total_number

        response["total_page"] = total_number // per_page + 1
        response["current_page"] = page

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/get_last', methods=['GET'])
def get_last():
    uuid = request.args.get('uuid', None, type=str)
    sort = request.args.get('sort', "all", type=str)
    user_role = request.args.get('user_role', "student", type=str)

    parameters = {
        "sort": sort,
        "uuid": uuid,
        "user_role": user_role,
    }

    response = {"ok": False}
    try:
        tasks = task_handler.get_last(parameters=parameters)
        if tasks == None:
            tasks = []
        response["ok"] = True
        response["tasks"] = tasks


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
            student = models.User.query.filter_by(uuid=task['student']).first()
            if student:
                task['student'] = student.to_dict()
            mentor = models.User.query.filter_by(uuid=task['mentor']).first()
            if mentor:
                task['mentor'] = mentor.to_dict()

        response["ok"] = True
        response["task"] = task
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

######## To delete 
########
@blueprint.route('/search_task', methods=['GET'] )
def search_task():
    query = request.args.get('query', None, type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    response = {"ok": False}
    try:
        tasks = task_handler.search_task(query=query, page=page, per_page=per_page)
       
        total_number = len(tasks)
        total_page = total_number // per_page + 1

        response['tasks'] = tasks
        response['total_number'] = total_number
        response["current_page"] = page
        response["total_page"] = total_page
        response["ok"] = True

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
########
#######

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
            mentor = models.User.query.filter_by(uuid=new_task.mentor).first()
            if mentor:
                response["task"]['mentor'] = mentor.to_dict()
            student = models.User.query.filter_by(uuid=new_task.student).first()
            if student:
                response["task"]['student'] = student.to_dict()
            
            
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
            response["ok"] = True
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
