import time

import models
from . import tools



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
 