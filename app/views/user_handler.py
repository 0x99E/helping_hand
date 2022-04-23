import datetime
import models
from . import tools

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


