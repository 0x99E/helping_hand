import time
import datetime
import models
from . import tools
from sqlalchemy import or_

allowed_task_changes = ["name", "description", "mentor"]
create_task_options = ["name", "description", "mentor", ]
search_task_options = ["name", "description", "mentor", "student", ]

def delete_task(parameters):
    try:
        session_token = parameters['session_token']
        task_uuid = parameters['uuid']
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            return None 
        user_uuid = session.uuid

        task_to_delete = models.Task.query.filter_by(uuid=task_uuid, student=user_uuid).first()
        if task_to_delete == None:
            return None
        models.db.session.delete(task_to_delete)
        models.db.session.commit()
    except:
        return None

def create_task(parameters):
    task = None
    try:
        session_token = parameters['session_token']
        task_options = parameters['task']
        try:
            mentor = task_options['mentor']
        except:
            raise Exception("No mentor specified")
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            raise Exception("Invalid session token")
        uuid = session.uuid
        
        
        new_task = models.Task()
        mentor_exists = bool(models.User.query.filter_by(uuid=mentor, mentor=True).first())
        if mentor_exists:
            pass
        else:
            raise Exception("Mentor does not exist")

        for key in task_options:
            value = task_options[key]
            if key in create_task_options:
                if key == "name":
                    new_task.name = value
                elif key == "description":
                    new_task.description = value
                elif key == "mentor":
                    new_task.mentor = value



        new_task.student = uuid
        task_exists = True
        while task_exists:
            uuid = "t_" + tools.random_string(20)
            task_exists = bool(models.Task.query.filter_by(uuid=uuid).first())
        
        new_task.uuid = uuid

        models.db.session.add(new_task)
        models.db.session.commit()

        return new_task
    except Exception as e:
        raise e

def search_task(parameters):
    tasks = None
    allowed_params = {}
    for key in parameters:
        if key in search_task_options:
            allowed_params[key] = parameters[key]
    
    like_params = []
    strong_params = {}
    for key in allowed_params:
        value = allowed_params[key]
        temp_param = None
        if key == "name":
            temp_param = models.Task.name.like("%" + value + "%")
            like_params.append(temp_param)

        elif key == "description":
            temp_param = models.Task.description.like("%" + value + "%")
            like_params.append(temp_param)
        else:
            strong_params[key] = value



    try:
        tasks = models.Task.query.filter(or_(*like_params), **strong_params).all()
        return tasks
    except Exception as e:
        raise e