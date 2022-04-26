import time
import datetime
import models
from . import tools
from sqlalchemy import or_

allowed_task_changes = ["name", "description", "answer", ]
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
    response = {}
    per_page = 10
    tasks = None
    allowed_params = {}
    page = 0
    if 'page' in parameters:
        page = parameters['page']
    
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
        rtasks = models.Task.query.filter(or_(*like_params), **strong_params)
        try:
            rtasks = rtasks.paginate(page, per_page, False).items
            total_number = len(rtasks)
        except:
            rtasks = []
            total_number = 0
        tasks = []
        for task in rtasks:
            task = task.to_dict()
            tasks.append(task)
        response['tasks'] = tasks
        response['total_number'] = total_number
        response["current_page"] = page
        response["total_page"] = total_number // per_page + 1
        
        return response
    except Exception as e:
        raise e

def close_task(parameters):
    try:
        session_token = parameters['session_token']
        task_uuid = parameters['uuid']
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            raise Exception("Invalid session token")
        user_uuid = session.uuid


        like_params = []
        like_params.append(
            models.Task.mentor == user_uuid,
        )

        

        task_to_close = models.Task.query.filter(
            ( (models.Task.mentor == user_uuid) | (models.Task.student == user_uuid) ),
            models.Task.uuid == task_uuid,
        ).first()
        if task_to_close == None:
            raise Exception("Task does not exist")

        task_to_close.closed = True
        models.db.session.commit()

        return task_to_close
    except Exception as e:
        raise e

def edit_task(parameters):
    try:
        session_token = parameters['session_token']
        task_uuid = parameters['uuid']
        task_params = parameters['task']
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            raise Exception("Invalid session token")
        user_uuid = session.uuid


        

        like_params = []
        like_params.append(
            models.Task.mentor == user_uuid,
        )
        like_params.append(
            models.Task.student == user_uuid,
        )

        

        task = models.Task.query.filter(
            or_(*like_params),
            models.Task.uuid == task_uuid,
            models.Task.closed == False,
        ).first()
        if task == None:
            raise Exception("Task does not exist or closed!")

        for key in task_params:
            value = task_params[key]
            if key in allowed_task_changes:
                if key == "name":
                    task.name = value
                elif key == "description":
                    task.description = value
                elif key == "answer":
                    task.answer = value

        models.db.session.commit()

        return task
    except Exception as e:
        raise e