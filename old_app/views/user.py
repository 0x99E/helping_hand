from flask import Blueprint
from flask import current_app
from flask import request
from flask import jsonify

import json

import models

from . import tools
from . import user_handler

blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.route('/get_user', methods=['GET'])
def get_user():
    uuid = request.args.get('uuid', None, type=str)

    response = {"ok": False}
    try:
        user = models.User.query.filter_by(uuid=uuid).first()
        if user == None:
            user = []
        else:
            user = user.to_dict()
        response["ok"] = True
        response["user"] = user
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

# Get all users with pagination
@blueprint.route('/get_users', methods=['GET'])
def get_users():
    per_page = 10
    page = request.args.get('page', 1, type=int)
    response = {"ok": False}
    try:
        total_number = models.User.query.count()
        raw_users = models.User.query.paginate(page, per_page, False).items
        users = []
        for user in raw_users:
            users.append(user.to_dict())
        response["ok"] = True
        response["users"] = users
        response["total"] = total_number
        response["current_page"] = page
        response["total_page"] = total_number // per_page + 1

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

# Get all mentors with pagination
@blueprint.route('/get_mentors', methods=['GET'])
def get_mentors():
    per_page = 10
    page = request.args.get('page', 1, type=int)
    response = {"ok": False}
    try:
        total_number = models.User.query.filter_by(mentor=True).count()
        raw_users = models.User.query.filter_by(mentor=True).paginate(page, per_page, False).items
        users = []
        for user in raw_users:
            users.append(user.to_dict())
        response["ok"] = True
        response["users"] = users
        response["total"] = total_number
        response["current_page"] = page
        response["total_page"] = total_number // per_page + 1

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

# Get all mentors with pagination
@blueprint.route('/get_topmentors', methods=['GET'])
def get_topmentors():
    response = {"ok": False}
    try:
        mentors_limit = 5
        filter_by = {}
        filter_by["mentor"] = True
        raw_mentors = models.User.query.filter_by(**filter_by).order_by(models.User.rating.desc()).limit(mentors_limit).all()
        
        mentors = []
        response["mentors"] = []

        for mentors in raw_mentors:
            ready_mentor = mentors.to_dict()
            response["mentors"].append(ready_mentor)


        response["ok"] = True

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    name = request.args.get('name', 0, type=str)
    photo = request.args.get('photo', 0, type=str)
    mentor = request.args.get('mentor', False, type=bool)
    service_token = request.args.get('service_token', 0, type=str)
    response = {"ok": False}
    try:
        valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
        if valid_request:
            user_exists = True
            while user_exists:
                uuid = "u_" + tools.random_string(20)
                user_exists = bool(models.User.query.filter_by(uuid=uuid).first())
            
            user = models.User(name=name, photo=photo, mentor=mentor, uuid=uuid)
            models.db.session.add(user)
            models.db.session.commit()
            response["ok"] = True
            response["user"] = user.to_dict()
        else:
            response["error"] = "Invalid service key"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/statistics', methods=['GET'])
def statistics():
    response = {"ok": False}
    try:
        total_mentor = models.User.query.filter_by(mentor=True).count()
        total_asker = models.User.query.filter_by(mentor=False).count()
        total_user = total_asker + total_mentor
        response["ok"] = True
        response["mentor"] = total_mentor
        response["asker"] = total_asker
        response["user"] = total_user

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/user_exists', methods=['GET'])
def user_exists():
    uuid = request.args.get('uuid', "", type=str)
    response = {"ok": False}
    try:
        user_exists = bool(models.User.query.filter_by(uuid=uuid).first())
        response["ok"] = True
        response["result"] = user_exists

    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)

@blueprint.route('/change_user', methods=['POST'])
def change_user():
    session_token = None
    parameters = None
    
    if request.is_json:
        try:
            raw_parameters = request.json
            # raw_parameters = json.loads(raw_parameters)
            session_token = raw_parameters['session_token']
            parameters = raw_parameters['user']
        except:
            pass
    
    response = {"ok": False}
    try:
        valid_request = bool(models.Session.query.filter_by(session_token=session_token).first())
        if valid_request:
            new_user = user_handler.change_user(session_token=session_token, user_options=parameters)
            if new_user:
                response["ok"] = True
                response["user"] = new_user.to_dict()
            else:
                response["error"] = "Cannot edit."
        else:
            response["error"] = "Invalid session_token"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
