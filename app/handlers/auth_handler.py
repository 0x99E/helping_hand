import time

import models

from . import session_handler
from . import tools


def login(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = {}



    token = None
    try:
        token = parameters['token']
    except:
        pass

    auth_object = models.Auth.query.filter_by(token=token).first()
    if auth_object == None:
        response["error"] = "Invalid token"
        return response
    
    uuid = auth_object.uuid
    new_session = create_session(uuid)
    user = models.User.query.filter_by(uuid=uuid).first()

    response["result"]["user"] = user.to_dict()
    response["result"]["session"] = new_session.to_dict()


    return response

def check_token(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = None

    token = None
    try:
        token = parameters['token']
    except:
        pass

    auth = models.Auth.query.filter_by(token=token).first()
    if auth:
        response["ok"] = True
        response['result'] = True
        
    else:
        response['result'] = False
    
    return response

def check_session_token(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = {}

    session_token = None
    try:
        session_token = parameters['session_token']
    except:
        pass


    new_session = None
    try:
        new_session = renew_session(session_token)
    except:
        pass

    if new_session:
        user = models.User.query.filter_by(uuid=new_session.uuid).first()

        if user:
            response["ok"] = True
            response['result']['user'] = user.to_dict()
            response['result']['session'] = new_session.to_dict()
        else:
            response["error"] = "User not found"
    else:
        response['error'] = "Session expired or invalid"

    return response

def logout(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = None

    session_token = None
    try:
        session_token = parameters['session_token']
    except:
        pass

    session = models.Session.query.filter_by(session_token=session_token).first()

    if session == None:
        response["result"] = False
    else:
        response["result"] = True
        models.db.session.delete(session)
        models.db.session.commit()

    
    

    response["ok"] = True
    return response



def not_expired_session(session_token):
    result = False
    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        pass

    if session.expire > time.time():
        result = True
    

    return result

def renew_session(session_token):
    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        return None
    
    session_valid = not_expired_session(session_token)
    if not session_valid:
        models.db.session.delete(session)
        models.db.session.commit()
        return None
    
    configs = models.Config.query.first()
    session_timeout = configs.session_timeout
    new_expire = time.time() + session_timeout
    new_expire = int(new_expire)
    session.expire = new_expire
    models.db.session.commit()

    return session

def create_session(uuid):
    session_exists = True
    while session_exists:
        session_token = "s_" + tools.random_string(20)
        session_exists = bool(models.Session.query.filter_by(session_token=session_token).first())
    
    configs = models.Config.query.first()
    session_timeout = configs.session_timeout
    new_expire = time.time() + session_timeout
    new_expire = int(new_expire)

    new_session = models.Session(uuid=uuid, session_token=session_token, expire=new_expire)
    models.db.session.add(new_session)
    models.db.session.commit()
    return new_session

