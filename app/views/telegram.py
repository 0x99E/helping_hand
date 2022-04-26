from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify
import json

import models

from . import tools
from . import user_handler

blueprint = Blueprint('telegram', __name__, url_prefix='/telegram')


@blueprint.route('/get_user', methods=['GET', 'POST'])
def get_user():
    service_token = None
    tgid = None
    
    if request.is_json:
        raw_parameters = request.json
        service_token = raw_parameters['service_token']
        tgid = raw_parameters['tgid']
    
    response = {"ok": False}
    try:
        valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
        if valid_request:
            user = models.TGUser.query.filter_by(tgid=tgid).first()
            if user:
                user = user.to_dict()
            response["ok"] = True
            response["user"] = user
        else:
            response["error"] = "Invalid service key"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/get_token', methods=['GET', 'POST'])
def get_token():
    service_token = None
    uuid = None
    
    if request.is_json:
        raw_parameters = request.json
        service_token = raw_parameters['service_token']
        uuid = raw_parameters['uuid']
    response = {"ok": False}
    try:
        valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
        if valid_request:
            user = models.Auth.query.filter_by(uuid=uuid).first()
            if user:
                # user = user.to_dict()
                response["ok"] = True
                response["token"] = user.token
            else:
                response["error"] = "Invalid uuid"
        else:
            response["error"] = "Invalid service key"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    service_token = None
    parameters = None
    
    if request.is_json:
        raw_parameters = request.json
        service_token = raw_parameters['service_token']
        parameters = raw_parameters['parameters']
    
    response = {"ok": False}
    try:
        valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
        if valid_request:
            new_user = user_handler.create_tguser(parameters)
            if new_user:
                response["ok"] = True
                response["user"] = new_user.to_dict()
            else:
                response["error"] = "Invalid parameters"
        else:
            response["error"] = "Invalid service key"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/statistics', methods=['GET'])
def statistics():
    response = {"ok": False}
    try:
        response["ok"] = True
        response["answer"] = "todo"
        

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/user_exists', methods=['GET', 'POST'])
def user_exists():
    tgid = request.args.get('tgid', "", type=str)
    service_token = request.args.get('service_token', 0, type=str)
    response = {"ok": False}
    try:
        valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
        if valid_request:
            user_exists = bool(models.TGUser.query.filter_by(tgid=tgid).first())
            response["ok"] = True
            response["result"] = user_exists
        else:
            response["error"] = "Invalid service key"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)


@blueprint.route('/change_user', methods=['GET', 'POST'])
def change_user():
    service_token = None
    parameters = None
    user = None
    uuid = None
    if request.is_json:
        raw_parameters = request.json
        service_token = raw_parameters['service_token']
        user = raw_parameters['user']
        uuid = user['uuid']
    
    response = {"ok": False}
    try:
        valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
        if valid_request:
            new_user = user_handler.change_user(uuid=uuid, user_options=user)

            if new_user:
                response["ok"] = True
                response["user"] = new_user.to_dict()
            else:
                response["error"] = "Invalid parameters"
        else:
            response["error"] = "Invalid service key"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
