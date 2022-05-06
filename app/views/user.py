from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify


import handlers


blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/get_user', methods=['GET'])
def get_user():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        response = handlers.USER.get_user(parameters)

    except:
        pass
    
    return jsonify(response)


@blueprint.route('/get_users', methods=['GET'])
def get_users():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)


    per_page = 10
    page = request.args.get('page', 1, type=int)

    parameters['page'] = page
    parameters['per_page'] = per_page

    try:
        response = handlers.USER.get_users(parameters)
    except:
        pass

    return jsonify(response)


@blueprint.route('/get_mentors', methods=['GET'])
def get_mentors():

    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)


    per_page = 10
    page = request.args.get('page', 1, type=int)

    parameters['page'] = page
    parameters['per_page'] = per_page


    try:
        response = handlers.USER.get_mentors(parameters)
    except:
        pass

    return jsonify(response)


@blueprint.route('/get_topmentors', methods=['GET'])
def get_topmentors():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        try:
            parameters.update(request.json)
        except:
            pass

    try:

        response = handlers.USER.get_topmentors(parameters)

    except:
        pass
    return jsonify(response)

@blueprint.route('/statistics', methods=['GET'])
def statistics():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        response = handlers.USER.statistics(parameters)
        
    except:
        pass
    return jsonify(response)


@blueprint.route('/user_exists', methods=['GET'])
def user_exists():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        
        response = handlers.USER.user_exists(parameters)

    except:
        pass
    return jsonify(response)


@blueprint.route('/change_user', methods=['POST'])
def change_user():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.USER.change_user(parameters)
    except:
        pass

    return jsonify(response)



# @blueprint.route('/create_user', methods=['GET', 'POST'])
# def create_user():
#     parameters = {}
#     response = {}

#     parameters.update(request.values)
#     if request.is_json:
#         parameters.update(request.json)

#     try:
#         response = handlers.USER.create_user(parameters)

#     except:
#         pass

#     return jsonify(response)

