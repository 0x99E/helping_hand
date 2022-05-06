from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify
import json


import models
import handlers

blueprint = Blueprint('telegram', __name__, url_prefix='/telegram')


@blueprint.route('/get_user', methods=['GET', 'POST'])
def get_user():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.TELEGRAM.get_user(parameters)

    except:
        pass
    return jsonify(response)

@blueprint.route('/get_token', methods=['GET', 'POST'])
def get_token():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.TELEGRAM.get_token(parameters)

    except:
        pass
    return jsonify(response)


@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.TELEGRAM.create_base_user(parameters)

    except:
        pass
    return jsonify(response)

@blueprint.route('/user_exists', methods=['POST'])
def user_exists():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)

    try:
        response = handlers.TELEGRAM.user_exists(parameters)

    except:
        pass
    return jsonify(response)


@blueprint.route('/change_user', methods=['GET', 'POST'])
def change_user():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)
    try:
        response = handlers.TELEGRAM.change_user(parameters)
    except:
        pass
    return jsonify(response)


@blueprint.route('/change_tguser', methods=['POST'])
def change_tguser():
    parameters = {}
    response = {}

    parameters.update(request.values)
    if request.is_json:
        parameters.update(request.json)
    try:
        response = handlers.TELEGRAM.change_tguser(parameters)
    except:
        pass
    
    return jsonify(response)
