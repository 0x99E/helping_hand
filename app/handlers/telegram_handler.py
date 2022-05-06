from multiprocessing import AuthenticationError
import time
import datetime

from requests import request
import models
from . import tools

allowed_user_changes = [
    "name", "photo", 
    "description", "mentor"
]

allowed_tguser_changes = [
    "photo", "photo_hash", 
    "known_photo", "known_photo_hash", 
]

def get_user(parameters):
    response = {}
    response["ok"] = False
    response["user"] = None

    telegram_id = None
    service_token = None
    try:
        telegram_id = parameters['tgid']
    except:
        pass

    try:
        service_token = parameters['service_token']
    except:
        pass


    valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
    if not valid_request:
        response["error"] = "Invalid service key"
        return response

    user = models.TGUser.query.filter_by(tgid=telegram_id).first()
    if user == None:
        response["error"] = "User not found"
        return response

    if user:
        user = user.to_dict()
    response["ok"] = True
    response["user"] = user
    return response

def get_token(parameters):
    response = {}
    response["ok"] = False
    response["token"] = None

    service_token = None
    uuid = None

    try:
        service_token = parameters['service_token']
    except:
        pass

    try:
        uuid = parameters['uuid']
    except:
        pass

    valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
    if not valid_request:
        response["error"] = "Invalid service key"
        return response


    authentication_record = models.Auth.query.filter_by(uuid=uuid).first()
    if authentication_record == None:
        response["error"] = "Authentication_record not found"
        return response

    response["ok"] = True
    response["token"] = authentication_record.token

    return response


def create_base_user(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["user"] = None
    response["tguser"] = None
    response["auth"] = None

    request_allowed = False
    request_allowed = is_service_token_valid(parameters)
    if not request_allowed:
        response["error"] = "Invalid service key"
        return response
    
    telegram_user = create_tguser(parameters)
    user = create_user(parameters)

    # REFACTOR
    auth = create_auth(parameters)

    response["ok"] = True
    response["user"] = user
    response["tguser"] = telegram_user
    response["auth"] = auth
    return response

def user_exists(parameters):
    response = {}
    response["ok"] = False
    response["result"] = None
    response["error"] = None


    request_allowed = False
    request_allowed = is_service_token_valid(parameters)
    if not request_allowed:
        response["error"] = "Invalid service key"
        return response
    

    telegram_id = None
    try:
        telegram_id = parameters['tgid']
    except:
        pass

    user_exists = bool(models.TGUser.query.filter_by(tgid=telegram_id).first())
    response["ok"] = True
    response["result"] = user_exists
    return response


def create_tguser(parameters):
    response = {}
    response["ok"] = False
    response["tguser"] = None

    first_name = None
    last_name = None
    username = None
    photo = None
    photo_hash = None
    known_photo = None
    tgid = None

    try:
        first_name = parameters["first_name"]
    except:
        pass

    try:
        last_name = parameters["last_name"]
    except:
        pass

    try:
        username = parameters["username"]
    except:
        pass

    try:
        photo = parameters["photo"]
    except:
        pass

    try:
        photo_hash = parameters["photo_hash"]
    except:
        pass

    try:
        known_photo = parameters["known_photo"]
    except:
        pass

    try:
        tgid = parameters["tgid"]
    except:
        pass


    # Get current time as a YYYY-MM-DD HH:MM:SS string
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M:%S")
    created_at = now_string
    tguser_exists = bool(models.TGUser.query.filter_by(tgid=tgid).first())
    if tguser_exists:
        return 0
    
    user = create_user(parameters)
    
    uuid = user.uuid
    new_tguser = models.TGUser(
    first_name=first_name,
    last_name=last_name, 
    username=username, 
    photo=photo, 
    tgid=tgid,
    uuid=uuid, 
    photo_hash=photo_hash, 
    known_photo=known_photo, 
    created_at=created_at
    )
    models.db.session.add(new_tguser)
    models.db.session.commit()
    
    response["ok"] = True
    response["user"] = user
    return response

def create_user(parameters):
    response = {}
    response["ok"] = False
    response["user"] = None

    name = None
    photo = None
    mentor = False
    
    try:
        name = parameters["first_name"]
    except:
        pass

    try:
        photo = parameters["photo"]
    except:
        pass

    try:
        mentor = parameters["mentor"]
    except:
        pass

    user_exists = True
    while user_exists:
        uuid = "u_" + tools.random_string(20)
        user_exists = bool(models.User.query.filter_by(uuid=uuid).first())
    
    new_user = models.User(name=name, photo=photo, mentor=mentor, uuid=uuid)
    models.db.session.add(new_user)
    models.db.session.commit()
    response["ok"] = True
    response["tguser"] = new_user

    return response

def create_auth(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["auth"] = None

    uuid = None
    try:
        uuid = parameters['uuid']
    except:
        pass

    try:
        uuid = parameters['user']['uuid']
    except:
        pass

    auth_object = models.Auth.query.filter_by(uuid=uuid).first()

    if auth_object != None:
        response["ok"] = True
        response["auth"] =  auth_object.to_dict()
        return response
    


    
    token = tools.random_string(20)
    new_auth = models.Auth(uuid=uuid, token=token)

    models.db.session.add(new_auth)
    models.db.session.commit()

    response["ok"] = True
    response["auth"] = new_auth.to_dict()

    return response

def is_service_token_valid(parameters):
    result = False

    service_token = None
    try:
        service_token = parameters['service_token']
    except:
        pass



    service_auth = models.SERVICEAuth.query.filter_by(token=service_token).first()
    result = bool(service_auth)

    return result





def check_user(uuid=None, tgid=None):
    check_by = ""

    if uuid != None:
        check_by = "uuid"
    elif tgid != None:
        check_by = "tgid"
    else:
        return 0
    
    if check_by == "uuid":
        auth = models.Auth.query.filter_by(uuid=uuid).first()
        if auth == None:
            create_auth(uuid)
    
    elif check_by == "tgid":
        tguser = models.TGUser.query.filter_by(tgid=tgid).first()
        uuid = tguser.uuid
        check_user(uuid)

def change_user(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["user"] = None

    allowed_request = False
    allowed_request = is_service_token_valid(parameters)
    if not allowed_request:
        response["error"] = "Invalid service key"
        return response

    session_token = None
    user_options = {}
    uuid = None

    try:
        session_token = parameters['session_token']
    except:
        pass
    
    try:
        uuid = parameters['uuid']
    except:
        pass

    try:
        user_options = parameters['user']
    except:
        pass

    if uuid == None:
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            response["error"] = "Invalid session token"
            return response
        uuid = session.uuid


    user = models.User.query.filter_by(uuid=uuid).first()
    if user == None:
        response["error"] = "User not found"
    
    
    for key in user_options:
        value = user_options[key]
        if key in allowed_user_changes:
            if key == "name":
                user.name = value
            elif key == "photo":
                if user.ignore_avatar:
                    pass
                else:
                    user.photo = value
            elif key == "description":
                user.description = value
    
    models.db.session.commit()

    response["ok"] = True
    response["user"] = user.to_dict()
    return response


def change_tguser(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["user"] = None

    allowed_request = False
    allowed_request = is_service_token_valid(parameters)
    if not allowed_request:
        response["error"] = "Invalid service key"
        return response
    

    user_options = {}
    telegram_id = None
    

    try:
        telegram_id = parameters['tgid']
    except:
        pass

    try:
        user_options = parameters['user']
    except:
        pass
    
    telegram_user = models.TGUser.query.filter_by(tgid=telegram_id).first()
    if telegram_user == None:
        response["error"] = "Telegram user not found"
        return response


    for key in user_options:
        value = user_options[key]
        if key in allowed_tguser_changes:
            if key == "photo":
                telegram_user.photo = value
            elif key == "photo_hash":
                telegram_user.photo_hash = value
            elif key == "known_photo":
                telegram_user.known_photo = value
            elif key == "known_photo_hash":
                telegram_user.known_photo_hash = value

    
    models.db.session.commit()
    response["ok"] = True
    response["user"] = telegram_user.to_dict()
    return response

