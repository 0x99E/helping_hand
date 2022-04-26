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
        full_url = self.base_url + "telegram/get_user"
        parameters = {
            "tgid": tgid,
            "service_token": self.service_token
        }
        resp = r.get(full_url, json=parameters)
        response = resp.json()
        result = None
        if response["ok"]:
            result = response["user"]
        else:
            result = None
        
        return result

    def get_token(self, uuid):
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
        return result

    def get_user(self, uuid):
        full_url = self.base_url + "user/get_user"
        parameters = {
            "uuid": uuid,
        }
        resp = r.get(full_url, params=parameters)
        response = resp.json()
        result = None
        if response["ok"]:
            result = response["user"]
        else:
            result = None
        
        return result

    def create_user(self, parameters):
        full_url = self.base_url + "telegram/create_user"
        parameters = {
            "parameters": parameters,
            "service_token": self.service_token
        }
        ready_parameters = parameters

        resp = r.post(full_url, json=ready_parameters)
        response = resp.json()
        result = None
        if response["ok"]:
            result = response["user"]
        else:
            result = None
        return result

    def tguser_exists(self, tgid):
        full_url = self.base_url + "telegram/user_exists"
        parameters = {
            "tgid": tgid,
            "service_token": self.service_token
        }
        resp = r.get(full_url, params=parameters)
        response = resp.json()
        result = None
        if response["ok"]:
            result = response["result"]
        else:
            result = None
        
        return result

    def user_exists(self, uuid):
        full_url = self.base_url + "user/user_exists"
        parameters = {
            "uuid": uuid,
        }
        resp = r.get(full_url, params=parameters)
        response = resp.json()
        result = None
        if response["status"] == "ok":
            result = response["result"]
        else:
            result = None
        
        return result