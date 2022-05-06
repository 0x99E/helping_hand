from flask import Blueprint
from flask import request
from flask import jsonify

import models
import handlers



blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# Get all users with pagination
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.AUTH.login(parameters)
        
    except:
        pass

    return jsonify(response)

@blueprint.route('/check_token', methods=['GET', 'POST'])
def check_token():

    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)
        
    try:

        response = handlers.AUTH.check_token(parameters)

    except:
        pass

    return jsonify(response)

@blueprint.route('/check_session_token', methods=['GET', 'POST'])
def check_session_token():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)
        

    try: 

        response = handlers.AUTH.check_session_token(parameters)
        
    except:
        pass

    return jsonify(response)

@blueprint.route('/logout', methods=['POST'])
def logout():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)
        
    try: 

        response = handlers.AUTH.logout(parameters)


    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

