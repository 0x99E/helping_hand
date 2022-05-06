
import requests as r
import json

class hh_api():
    def __init__(
            self, 
            base_url,
            service_token
        ):
        self.base_url = base_url
        self.service_token = service_token
    
    def get_tguser(self, tgid):
        result = None
        try:
            full_url = self.base_url + "telegram/get_user"
            parameters = {
                "tgid": tgid,
                "service_token": self.service_token
            }
            resp = r.get(full_url, json=parameters)
            response = resp.json()
            if response["ok"]:
                result = response["user"]
            else:
                result = None
        except Exception as e:
            print(e)
            pass 

        return result

    def get_user(self, uuid):
        result = None
        try:
            full_url = self.base_url + "user/get_user"
            parameters = {
                "uuid": uuid,
            }
            resp = r.get(full_url, params=parameters)
            response = resp.json()
            if response["ok"]:
                result = response["user"]
            else:
                result = None
            
            return result
        except:
            pass
        return result

    def edit_user(self, uuid, user):
        result = None
        try:
            full_url = self.base_url + "telegram/change_user"
            parameters = {
                "service_token": self.service_token,
                "uuid": uuid,
                "user": user,
            }
            resp = r.post(full_url, json=parameters)
            response = resp.json()
            if response["ok"]:
                result = response["user"]
            else:
                result = None
        except:
            pass
        return result

    def edit_tguser(self, tgid, user):
        result = None
        try:
            full_url = self.base_url + "telegram/change_tguser"
            parameters = {
                "service_token": self.service_token,
                "tgid": tgid,
                "user": user,
            }


            resp = r.post(full_url, json=parameters)
            response = resp.json()
            if response["ok"]:
                result = response["user"]
            else:
                result = None
        except Exception as e:
            print(e)
        return result

    def create_user(self, parameters):
        result = None
        try:
            full_url = self.base_url + "telegram/create_user"
            parameters = {
                "parameters": parameters,
                "service_token": self.service_token
            }
            ready_parameters = parameters

            resp = r.post(full_url, json=ready_parameters)
            response = resp.json()
            if response["ok"]:
                result = response["user"]
            else:
                result = None
            return result
        except:
            pass
        return result

    def tguser_exists(self, tgid):
        result = None
        try:
            full_url = self.base_url + "telegram/user_exists"
            parameters = {
                "tgid": tgid,
                "service_token": self.service_token
            }
            resp = r.post(full_url, json=parameters)
            response = resp.json()
            if response["ok"]:
                result = response["result"]
            else:
                result = None
        except:
            pass
        return result

    def user_exists(self, uuid):
        result = None
        try:
            full_url = self.base_url + "user/user_exists"
            parameters = {
                "uuid": uuid,
            }
            resp = r.get(full_url, params=parameters)
            response = resp.json()
            if response["ok"]:
                result = response["result"]
            else:
                result = None
        except:
            pass
        return result
   
    def get_token(self, uuid):
        result = None
        try:
            full_url = self.base_url + "telegram/get_token"
            parameters = {
                "uuid": uuid,
                "service_token": self.service_token
            }
            
            resp = r.post(full_url, json=parameters)
            response = resp.json()
            result = None
            if response["ok"]:
                result = response["token"]
            else:
                result = None
        except:
            pass
        return result
     

class imgbb_api():
    def __init__(self, api_key):
        self.api_key = api_key

    def upload(self, image):
        result = None
        try:
            full_url = "https://api.imgbb.com/1/upload?key=" + self.api_key
            parameters = {
                "image": image
            }
            resp = r.post(full_url, data=parameters)
            response = resp.json()
            result = response

        except Exception as e:
            print(e)
        return result
        
