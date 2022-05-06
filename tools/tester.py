import requests
import random
import string

base_url = "http://127.0.0.1:5000/"
secret = "testtokentoken"

student_id = "u_test"

def random_str(n=15):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

def create_user():
    username = input("Enter username: ")
    photo = input("Enter photo: ")
    mentor = False
    if input("Is mentor? (y/n): ") == "y":
        mentor = True
    else:
        mentor = False
    url = base_url + "user/create_user"
    params = {
        "name": username,
        "photo": photo,
        "mentor": mentor,
        "service_key": secret
    }
    r = requests.get(url, params=params)
    print(r.text)

def create_users():
    for i in range(15):
        username = "temp_" + random_str()
        photo = random_str()
        mentor = False
        url = base_url + "user/create_user"
        params = {
            "name": username,
            "photo": photo,
            "mentor": mentor,
            "service_key": secret
        }
        r = requests.get(url, params=params)
        print(r.text)

# Create menu
def get_users():
    url = base_url + "user/get_users"
    response = requests.get(url)
    print(response.text)

def create_task():
    url = base_url + "task/create_task"
    name = input("Enter name: ")
    description = input("Enter description: ")
    session_token = input("Enter session: ")
    mentor = input("Enter mentor: ")
    params = {
        "session_token": session_token,
        "task": {
            "name": name,
            "description": description,
            "mentor": mentor,
            }
    }
    r = requests.post(url, json=params)
    print(r.text)

def create_tasks():
    for i in range(15):
        name = "temp_" + random_str()
        description = random_str()
        url = base_url + "task/create_task"
        params = {
            "name": name,
            "description": description,
            "student": student_id,
        }
        r = requests.get(url, params=params)
        print(r.text)

def get_tasks():
    url = base_url + "task/get_tasks"
    r = requests.get(url)
    print(r.text)

def search_task():
    url = base_url + "task/search_task"
    params = {}
    name = input("Enter name: ")
    description = input("Enter description: ")
    mentor = input("Enter mentor: ")
    if name != "":
        params["name"] = name
    if description != "":
        params["description"] = description
    if mentor != "":
        params["mentor"] = mentor

    
    r = requests.post(url, json=params)
    print(r.text)

def menu():
    print("1. Create user")
    print("2. Get users")
    print("3. Create users")
    print("4. Create task")
    print("5. Create tasks")
    print("6. Get tasks")
    print("7. Search task")
    print("0. Exit")

    option = input("Enter option: ")
    try:
        option = int(option)
    except:
        return 0

    if option == 1:
        create_user()
    elif option == 2:
        get_users()
    elif option == 3:
        create_users()
    elif option == 4:
        create_task()
    elif option == 5:
        create_tasks()
    elif option == 6:
        get_tasks()
    elif option == 7:
        search_task()
    
    elif option == 0:
        return 0
    
while 1:
    menu()