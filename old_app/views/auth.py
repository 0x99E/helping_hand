from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify

import models

from . import tools
from . import user_handler

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# Get all users with pagination
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    response = {"ok": False}
    try:
        token = request.values.get('token', "", type=str)
        if request.is_json:
            raw_parameters = request.json
            token = raw_parameters['token']

        auth = models.Auth.query.filter_by(token=token).first()
        if auth:
            new_session = user_handler.create_session(auth.uuid)
            new_user = models.User.query.filter_by(uuid=auth.uuid).first()

            response["ok"] = True
            response['result'] = {}
            response["result"]["session"] = new_session.to_dict()
            response["result"]["user"] = new_user.to_dict()
            
        else:
            response["error"] = "Invalid token"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/check_token', methods=['GET', 'POST'])
def check_token():
    token = request.values.get('token', "", type=str)

    response = {"ok": False}
    try:
        auth = models.Auth.query.filter_by(token=token).first()
        if auth:
            response["ok"] = True
            response['result'] = True
            
        else:
            response['result'] = False
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/check_session_token', methods=['GET', 'POST'])
def check_session_token():
    response = {"ok": False}
    try: 
        session_token = request.values.get('session_token', "", type=str)
        if request.is_json:
            raw_parameters = request.json
            session_token = raw_parameters['session_token']
        
        new_session = user_handler.renew_session(session_token)
        user = models.User.query.filter_by(uuid=new_session.uuid).first()
        if new_session:
            if user:
                response["ok"] = True
                response['result'] = {}
                response['result']['user'] = user.to_dict()
                response['result']['session'] = new_session.to_dict()
        else:
            response['error'] = "Session expired or invalid"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/logout', methods=['POST'])
def logout():
    response = {"ok": False}
    try: 
        session_token = request.values.get('session_token', "", type=str)
        if request.is_json:
            raw_parameters = request.json
            session_token = raw_parameters['session_token']
        
        response["ok"] = True   
        user_handler.logout(session_token)


    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

