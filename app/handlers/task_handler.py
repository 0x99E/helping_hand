import time
import datetime
import models
from . import tools
from sqlalchemy import or_, and_

allowed_task_changes = ["name", "description", "answer", "status" ]
create_task_options = ["name", "description", "mentor", ]
search_task_options = ["name", "description", "mentor", "student", ]
search_task_hardoptions = ["student", "mentor", "sort"]


def get_tasks(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None

    per_page = 10
    page = None

    query = None
    sort = None
    mentor = None
    student = None

    try:
        page = int(parameters['page'])
    except:
        page = 0
    
    try:
        sort = parameters['sort']
    except:
        sort = "all"

    try:
        mentor = parameters['mentor']
    except:
        pass

    try:
        student = parameters['student']
    except:
        pass



    total_number = models.Task.query.count()
    raw_tasks = models.Task.query.paginate(page, per_page, False).items
    tasks = []
    for task in raw_tasks:
        try:
            ready_task = task.to_dict()

            mentor_uuid = ready_task['mentor']
            try:
                mentor = models.User.query.filter_by(uuid=mentor_uuid).first()
                mentor = mentor.to_dict()
            except:
                mentor = None
            ready_task['mentor'] = mentor


            student_uuid = ready_task['student']
            try:
                student = models.User.query.filter_by(uuid=student_uuid).first()
                student = student.to_dict()
            except:
                student = None
            ready_task['student'] = student

            tasks.append(ready_task)
        except Exception as e:
            print(e)

        
    
    response["ok"] = True
    response["tasks"] = tasks
    response["total"] = total_number
    response["current_page"] = page
    response["total_page"] = total_number // per_page + 1

    return response

def get_task(parameters):

    response = {}
    response["ok"] = False
    response["error"] = None
    response["task"] = None

    uuid = None

    try:
        uuid = parameters['uuid']
    except:
        pass

    task = models.Task.query.filter_by(uuid=uuid).first()
    if task == None:
        task = []
    else:
        task = task.to_dict()
        student = models.User.query.filter_by(uuid=task['student']).first()
        if student:
            task['student'] = student.to_dict()
        mentor = models.User.query.filter_by(uuid=task['mentor']).first()
        if mentor:
            task['mentor'] = mentor.to_dict()

    response["ok"] = True
    response["task"] = task

    return response

def create_view( response = None, content_type = None):
    if content_type == "task":
        task = response['task']

        task_mentor_uuid = None
        task_student_uuid = None

        try:
            task_mentor_uuid = task['mentor']
        except:
            pass
        try:
            task_student_uuid = task['student']
        except:
            pass
        
        try:
            if task_mentor_uuid != None:
                task_mentor = models.User.query.filter_by(uuid=task_mentor_uuid).first()
                if task_mentor != None:
                    task['mentor'] = task_mentor.to_dict()
        except:
            pass

        try:
            if task_student_uuid != None:
                task_student = models.User.query.filter_by(uuid=task_student_uuid).first()
                if task_student != None:
                    task['student'] = task_student.to_dict()
        except:
            pass

        return response


def get_last(parameters):

    response = {}
    response["ok"] = False
    response["error"] = None
    response["tasks"] = None

    num_limit = 5

    try:
        uuid = parameters['uuid']
    except:
        pass

    try:
        sort = parameters['sort']
    except:
        sort = "all"

    try:
        user_role = parameters['user_role']
    except:
        user_role = "student"



    try:
        search_by = []
        if user_role == "mentor":
            search_by.append(models.Task.mentor == uuid)
        else:
            search_by.append(models.Task.student == uuid)


        try:
            t_sort = sort.lower()
            if t_sort in ['open', 'closed']:
                b_value = True if t_sort == 'closed' else False
                search_by.append(models.Task.closed == b_value)
            else:
                pass
        except:
            pass
        
        ready_tasks = []
        Obj_tasks = models.Task.query.filter(*search_by).limit(num_limit)
        if Obj_tasks != None:
            raw_tasks = Obj_tasks.all()
            for task in raw_tasks:
                try:
                    task_mentor_uuid = task.mentor
                    task_student_uuid = task.student
                    task_mentor = models.User.query.filter_by(uuid=task_mentor_uuid).first()
                    task_student = models.User.query.filter_by(uuid=task_student_uuid).first()
                    try:
                        task_mentor = task_mentor.to_dict()
                    except:
                        task_mentor = []
                    try:
                        task_student = task_student.to_dict()
                    except:
                        task_student = []
                    task_dict = task.to_dict()
                    task_dict['mentor'] = task_mentor
                    task_dict['student'] = task_student
                    ready_tasks.append(task_dict)
                except:
                    pass
        
        response["ok"] = True
        response["tasks"] = ready_tasks

    except Exception as error:
        error_msg = str(error)
        response["error"] = error_msg
    
    return response

def delete_task(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None

    session_token = None
    task_uuid = None
    try:
        task_uuid = parameters['uuid']
    except:
        pass

    try:
        session_token = parameters['session_token']
    except:
        pass

    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        response["error"] = "Invalid session token"
        return response

    user_uuid = session.uuid

    task_to_delete = models.Task.query.filter_by(uuid=task_uuid, student=user_uuid).first()
    if task_to_delete == None:
        response["error"] = "Task not found"
        return response
    
    models.db.session.delete(task_to_delete)
    models.db.session.commit()

    response["ok"] = True

    return response

def create_task(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["task"] = None

    session_token = None
    task_options = None
    mentor_uuid = None
    try:
        session_token = parameters['session_token']
    except:
        pass

    try:
        task_options = parameters['task']
    except:
        pass

    try:
        mentor_uuid = task_options['mentor']
    except:
        pass


    try:

        if mentor_uuid == None:
            response["error"] = "No mentor specified."
            return response

        if session_token == None:
            response["error"] = "No session token specified."
            return response
        
        if task_options == None:
            response["error"] = "No task options specified."
            return response
        
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            response["error"] = "Invalid session token."
            return response
        

        student_uuid = session.uuid
        
        

        mentor_exists = bool(models.User.query.filter_by(uuid=mentor_uuid, mentor=True).first())
        if not mentor_exists:
            response["error"] = "Mentor does not exist."
            return response
        

        new_task = models.Task()

        for key in task_options:
            value = task_options[key]
            if key in create_task_options:
                if key == "name":
                    new_task.name = value
                elif key == "description":
                    new_task.description = value
                elif key == "mentor":
                    new_task.mentor = value

        new_task.student = student_uuid

        task_exists = True
        task_uuid = None
        while task_exists:
            task_uuid = "t_" + tools.random_string(20)
            task_exists = bool(models.Task.query.filter_by(uuid=task_uuid).first())
        
        new_task.uuid = task_uuid
        current_time = str(datetime.datetime.now())
        current_int_time = time.time()
        new_task.date = current_time
        new_task.idate = current_int_time
        models.db.session.add(new_task)
        models.db.session.commit()

        response["ok"] = True
        response["task"] = new_task.to_dict()
        return response
    except:
        return response

def search_task(query, page, per_page, parameters):
    result = {}
    result["ok"] = False
    result["error"] = None

    result['tasks'] = []
    query = str(query)
                             
    like_params = [
        models.Task.name.like("%" + query + "%"),
        models.Task.description.like("%" + query + "%"),
    ]

    hard_params = []
    for key in parameters:
        value = parameters[key]
        if value == None:
            continue
        if key in search_task_hardoptions:
            if key == "student":
                hard_params.append(models.Task.student == value)
            elif key == "mentor":
                hard_params.append(models.Task.mentor == value)
            elif key == "sort":
                value = value.lower()
                if value in ['open', 'closed']:
                    b_value = True if value == 'closed' else False
                    hard_params.append(models.Task.closed == b_value)
                else:
                    pass

    ready_tasks = []
    info = {}
    info['total'] = 0
    try:
        qtasks = models.Task.query.filter(and_(or_(*like_params), *hard_params)).order_by(models.Task.idate.desc())
        info['total'] = qtasks.count()
        try:
            rtasks = qtasks.paginate(page, per_page, False).items
        except:
            rtasks = []
        
        for task in rtasks:
            try:
                task_mentor_uuid = task.mentor
                task_student_uuid = task.student
                task_mentor = models.User.query.filter_by(uuid=task_mentor_uuid).first()
                task_student = models.User.query.filter_by(uuid=task_student_uuid).first()
                try:
                    task_mentor = task_mentor.to_dict()
                except:
                    task_mentor = []
                try:
                    task_student = task_student.to_dict()
                except:
                    task_student = []
                task_dict = task.to_dict()
                task_dict['mentor'] = task_mentor
                task_dict['student'] = task_student
                ready_tasks.append(task_dict)
            except:
                pass
        
        result['tasks'] = ready_tasks
        result['info'] = info
        return result
    except Exception as e:
        raise e

def close_task(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["task"] = None

    session_token = None
    task_uuid = None
    try:
        session_token = parameters['session_token']
    except:
        pass

    try:
        task_uuid = parameters['uuid']
    except:
        pass

    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        response["error"] = "Invalid session token"
        return response

    user_uuid = session.uuid


    task_to_close = models.Task.query.filter(models.Task.uuid == task_uuid).first()
    if task_to_close == None:
        response["error"] = "Task not found"
        return response

    allowed_to_close = bool((task_to_close.student == user_uuid) |  (task_to_close.mentor == user_uuid))
    if allowed_to_close:
        task_to_close.closed = True
        models.db.session.commit()
    
    else:
        response["error"] = "You are not allowed to close this task"
        return response

    response["ok"] = True
    response["task"] = task_to_close.to_dict()
    return response
    

def edit_task(parameters):
    response = {}
    response["ok"] = False
    response["error"] = None
    response["task"] = None

    session_token = None
    task_uuid = None
    task_parameters = []
    try:
        session_token = parameters['session_token']
    except:
        pass

    try:
        task_uuid = parameters['uuid']
    except:
        pass

    try:
        task_parameters = parameters['task']
    except:
        pass


    session = models.Session.query.filter_by(session_token=session_token).first()
    if session == None:
        response["error"] = "Invalid session token"
        return response

    user_uuid = session.uuid

    


    # REFACTOR
    task = models.Task.query.filter(
        models.Task.uuid == task_uuid,
    ).first()

    if task == None:
        response["error"] = "Task not found"
        return response

    for key in task_parameters:
        value = task_parameters[key]
        if key in allowed_task_changes:
            if key == "name":
                task.name = value
            elif key == "description":
                task.description = value
            elif key == "answer":
                task.answer = value
            elif key == "status":
                if value in ['open', 'closed']:
                    b_value = True if value == 'closed' else False
                    task.closed = b_value

    models.db.session.commit()

    response["ok"] = True
    response["task"] = task.to_dict()

    mentor_uuid = task.mentor
    student_uuid = task.student
    try:
        mentor = models.User.query.filter_by(uuid=mentor_uuid).first()
        mentor = mentor.to_dict()
    except:
        mentor = None

    try:
        student = models.User.query.filter_by(uuid=student_uuid).first()
        student = student.to_dict()
    except:
        student = None
    
    response["task"]["mentor"] = mentor
    response["task"]["student"] = student
    
    return response
