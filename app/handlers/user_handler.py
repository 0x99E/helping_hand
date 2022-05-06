import time
import datetime
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
    response["error"] = None
    response["result"] = None

    uuid = None
    try:
        uuid = parameters['uuid']
    except:
        pass

    user = models.User.query.filter_by(uuid=uuid).first()

    if user == None:
        user = []
    else:
        user = user.to_dict()
    
    response["ok"] = True
    response["user"] = user

    return response

def get_users(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = None

    try:
        page = parameters['page']
    except:
        page = 0

    try:
        per_page = parameters['per_page']
    except:
        per_page = 10
    

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

    return response

def get_mentors(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None

    try:
        page = parameters['page']
    except:
        page = 0

    try:
        per_page = parameters['per_page']
    except:
        per_page = 10
    

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

    return response

def get_topmentors(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["mentors"] = []


    mentors_limit = 5
    filter_by = {}
    filter_by["mentor"] = True
    raw_mentors = models.User.query.filter_by(mentor=True).order_by(models.User.rating.desc()).limit(mentors_limit).all()
    
    mentors = []

    for mentors in raw_mentors:
        ready_mentor = mentors.to_dict()
        response["mentors"].append(ready_mentor)

    response["ok"] = True

    return response

def create_user(parameters):

    response = {}
    response["ok"] = False
    response["error"] = None
    response["user"] = None

    try:
        name = parameters["first_name"]
    except:
        name = None
    
    try:
        photo = parameters["photo"]
    except:
        photo = None
    
    try:
        mentor = parameters["mentor"]
    except:
        mentor = None
    
    try:
        service_token = parameters["service_token"]
    except:
        service_token = None

    valid_request = bool(models.SERVICEAuth.query.filter_by(token=service_token).first())
    if valid_request:
        user_exists = True
        while user_exists:
            uuid = "u_" + tools.random_string(20)
            user_exists = bool(models.User.query.filter_by(uuid=uuid).first())
        
        new_user = models.User(name=name, photo=photo, mentor=mentor, uuid=uuid)
        models.db.session.add(new_user)
        models.db.session.commit()

        try:
            auth = create_auth(uuid)
        except:
            pass
            
        response["user"] = new_user.to_dict()
        response["ok"] = True


    else:
        response["error"] = "Invalid service token"


    return response

def statistics(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = None

    total_mentor = models.User.query.filter_by(mentor=True).count()
    total_asker = models.User.query.filter_by(mentor=False).count()
    total_user = total_asker + total_mentor

    response["ok"] = True
    response["mentor"] = total_mentor
    response["asker"] = total_asker
    response["user"] = total_user

    return response

def user_exists(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["result"] = None

    uuid = None
    try:
        uuid = parameters['uuid']
    except:
        pass

    user_exists = bool(models.User.query.filter_by(uuid=uuid).first())
    response["ok"] = True
    response["result"] = user_exists

    return response

def change_user(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["user"] = None


    session_token = None
    try:
        session_token = parameters['session_token']
    except:
        pass


    valid_request = bool(models.Session.query.filter_by(session_token=session_token).first())
    if valid_request:
        new_user = change_user(session_token=session_token, user_options=parameters)
        if new_user:
            response["ok"] = True
            response["user"] = new_user.to_dict()
        else:
            response["error"] = "Cannot edit."
    else:
        response["error"] = "Invalid session_token"
    
    return response

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

def change_user(session_token=None, uuid=None, user_options=None):
    user = None
    if not uuid:
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            return None
        uuid = session.uuid
    
    user = models.User.query.filter_by(uuid=uuid).first()
    if user == None:
        return None
    
    
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

    return user

def change_tguser(tgid=None, user_options=None):

    user = models.TGUser.query.filter_by(tgid=tgid).first()
    if user == None:
        return None
    

    for key in user_options:
        value = user_options[key]
        if key in allowed_tguser_changes:
            if key == "photo":
                user.photo = value
            elif key == "photo_hash":
                user.photo_hash = value
            elif key == "known_photo":
                user.known_photo = value
            elif key == "known_photo_hash":
                user.known_photo_hash = value

    
    models.db.session.commit()

    return user

def logout(session_token):
    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        return None
    
    models.db.session.delete(session)
    models.db.session.commit()
    return True

