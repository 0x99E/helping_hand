import time
import datetime
import models
from . import tools

allowed_user_changes = ["name", "photo", "description", "mentor"]
allowed_tguser_changes = [
    "photo", "photo_hash", 
"known_photo", "known_photo_hash", 
]

def create_tguser(parameters):
    first_name = parameters["first_name"]
    last_name = parameters["last_name"]
    username = parameters["username"]
    photo = parameters["photo"]
    photo_hash = parameters["photo_hash"]
    known_photo = parameters["known_photo"]
    tgid = parameters["tgid"]
    # Get current time as a YYYY-MM-DD HH:MM:SS string
    now = datetime.datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M:%S")
    created_at = now_string
    tguser_exists = bool(models.TGUser.query.filter_by(tgid=tgid).first())
    if tguser_exists:
        return 0
    
    user_login = first_name
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
    return new_tguser

def create_user(parameters):
    response = {}
    response["ok"] = False
    name = parameters["first_name"]
    photo = parameters["photo"]
    mentor = parameters["mentor"]
    
    user_exists = True
    while user_exists:
        uuid = "u_" + tools.random_string(20)
        user_exists = bool(models.User.query.filter_by(uuid=uuid).first())
    
    new_user = models.User(name=name, photo=photo, mentor=mentor, uuid=uuid)
    models.db.session.add(new_user)
    models.db.session.commit()

    auth = create_auth(uuid)

    return new_user

def create_auth(uuid,):
    auth_exists = bool(models.Auth.query.filter_by(uuid=uuid).first())

    if auth_exists:
        return 0
    
    token = tools.random_string(20)
    new_auth = models.Auth(uuid=uuid, token=token)
    models.db.session.add(new_auth)
    models.db.session.commit()
    return new_auth

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

def create_session(uuid):
    check_user(uuid=uuid)

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


def new_session(uuid):
    check_user(uuid=uuid)
    new_session = create_session(uuid)
    return new_session

def logout(session_token):
    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        return None
    
    models.db.session.delete(session)
    models.db.session.commit()
    return True