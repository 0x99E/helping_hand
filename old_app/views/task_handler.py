import time
import datetime
import models
from . import tools
from sqlalchemy import or_, and_

allowed_task_changes = ["name", "description", "answer", ]
create_task_options = ["name", "description", "mentor", ]
search_task_options = ["name", "description", "mentor", "student", ]
search_task_hardoptions = ["student", "mentor", "sort"]

def get_last(parameters):
    tasks = []
    try:
        num_limit = 5
        uuid = parameters['uuid']
        sort = parameters['sort']
        user_role = parameters['user_role']

        search_by = []
        if user_role == "mentor":
            search_by.append(models.Task.mentor == uuid)
        else:
            search_by.append(models.Task.student == uuid)

        try:
            value = sort
            value = value.lower()
            if value in ['open', 'closed']:
                b_value = True if value == 'closed' else False
                search_by.append(models.Task.closed == b_value)
            else:
                pass
        except:
            pass

        qtasks = models.Task.query.filter(*search_by).limit(num_limit)
        if qtasks != None:
            rtasks = qtasks.all()
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
                    tasks.append(task_dict)
                except:
                    pass
        
        return tasks
    except Exception as e:
        print(e)
        return tasks


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
        current_time = str(datetime.datetime.now())
        current_int_time = time.time()
        new_task.date = current_time
        new_task.idate = current_int_time
        models.db.session.add(new_task)
        models.db.session.commit()

        return new_task
    except Exception as e:
        raise e

def search_task(query, page, per_page, parameters):
    result = {}
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
    try:
        session_token = parameters['session_token']
        task_uuid = parameters['uuid']
        session = models.Session.query.filter_by(session_token=session_token).first()
        if session == None:
            raise Exception("Invalid session token")
        user_uuid = session.uuid


        

        task_to_close = models.Task.query.filter(
            models.Task.uuid == task_uuid,
        ).first()
        if task_to_close != None:
            allowed_to_close = bool((task_to_close.student == user_uuid) |  (task_to_close.mentor == user_uuid))
            if allowed_to_close:
                task_to_close.closed = True
                models.db.session.commit()
        else:
            raise Exception("Task does not exist")

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