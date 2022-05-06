import random
import config
import os
import base64
import message_template
import threading
import string

class Handler():
    def __init__(self, bot=None, hh_api=None, imgbb_api=None):
        self.bot = bot
        self.hh_api = hh_api
        self.imgbb_api = imgbb_api
    
    def random_str(self, size=10):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(size))

    def filter_str(self, raw_string):
        ready_string = ""
        try:
            allowed_chars = string.ascii_letters + string.digits + " "
            for char in raw_string:
                if char in allowed_chars:
                    ready_string += char
        except:
            pass
        return ready_string

    def handle(self, message):
        self.user_hander(message)

        self.cmd_handler(message)
        # Run in thread
        thr_photo_process = threading.Thread(target=self.photo_handle, args=(message,))
        thr_photo_process.start()
        
    def user_hander(self, message):
        tgid = message.from_user.id
        uuid = None

        tg_user_exists = None

        tg_user_exists = self.hh_api.tguser_exists(tgid)

        if tg_user_exists:
            tguser = self.hh_api.get_tguser(tgid)
            uuid = tguser["uuid"]
            user = self.hh_api.get_user(uuid)
        else:
            user = self.create_user(message)

        return user

    def cmd_handler(self, message):
        text = message.text
        tguser = self.parse_user(message, no_photo=True)
        chat_id = message.chat.id
        reply = ""

        name = tguser["first_name"]
        user = self.hh_api.get_tguser(tgid=tguser["tgid"])
        token = "no_token"
        try:
            token = self.hh_api.get_token(user['uuid'])
        except:
            pass
        
        link = config.web_url + "auth/" + token
        reply = message_template.default
        reply = reply.format(name=name, link=link, token=token)
        self.bot.send_message(chat_id, reply, parse_mode="HTML")

    def create_user(self, message):
        parameters = {}
        parameters = self.parse_user(message, no_photo=True)
        user = self.hh_api.create_user(parameters)
        return user

    def parse_user(self, message, no_photo=False):
        result = {}
        result["first_name"] = self.filter_str(message.from_user.first_name)
        result["last_name"] = self.filter_str(message.from_user.last_name)
        result["username"] = message.from_user.username
        result["mentor"] = False
        result["tgid"] = message.from_user.id
        result["photo"] = ""
        result["photo_hash"] = ""
        result["known_photo"] = ""
        result["known_photo_hash"] = ""

        return result

    def get_current_photo(self, message, only_hash=False):
        result = {}
        result["exists"] = False
        result["photo"] = None
        result["photo_hash"] = None
        try:

            tgid = message.from_user.id
            user_photos = self.bot.get_user_profile_photos(tgid)
            photo = user_photos.photos[0][0]

            photo_id = photo.file_id
            photo_hash = photo.file_unique_id

            result["exists"] = True
            result["photo_hash"] = photo_hash

            if only_hash:
                return result
            else:
                photo_file = self.bot.get_file(photo_id)
                photo_file_path = photo_file.file_path

                bphoto = self.bot.download_file(file_path=photo_file_path)
                # Create full path to photo
                bbasephoto = base64.b64encode(bphoto)
                bbasephoto = bbasephoto.decode("utf-8")
                # bbasephoto = "data:image/png;base64," + bbasephoto
                result["photo"] = bbasephoto

        except Exception as e:
            print(e)

        return result
    
    def get_last_photo(self, tgid, only_hash=False):
        tguser = self.hh_api.get_tguser(tgid)
       
        last_photo = {}
        last_photo['photo'] = None
        last_photo['photo_hash'] = None
        
        try:
            last_photo['photo_hash'] = tguser['photo_hash']
            if only_hash:
                pass
            else:
                last_photo['photo'] = tguser['photo']
        except:
            pass
        return last_photo

    def upload_photo(self, photo):
        image_data = None
        try:
            upload_info = self.imgbb_api.upload(photo)
            if upload_info != None:
                if upload_info['success']:
                    img_info = upload_info['data']
                    image_data = img_info['url']
        except:
            pass

        return image_data

    def update_photo(self, message):
        tgid = message.from_user.id
        tguser = self.hh_api.get_tguser(tgid)
        if tguser == None:
            return
        uuid = tguser['uuid']
        current_photo = self.get_current_photo(message)
        current_photo_hash = current_photo['photo_hash']

        upload_info = {}
        photo_data = None
        if current_photo['exists']:
            photo_bytes = current_photo['photo']
            photo_data = self.upload_photo(photo_bytes)
        
        if photo_data == None:
            return 0
        
        tguser_info = {
            'photo': photo_data,
            'photo_hash': current_photo_hash
        }
    
        self.hh_api.edit_tguser(tgid, tguser_info)
        self.hh_api.edit_user(uuid, tguser_info)

    # unused
    def process_photos(self, message):
        tgid = message.from_user.id
        user_photos = self.bot.get_user_profile_photos(tgid)
        # photo = user_photos.photos[0][0]
        print(len(user_photos.photos))

    def photo_handle(self, message):
        try:
            tgid = message.from_user.id
            print("photo_handle")
            print(tgid)

            tguser = self.hh_api.get_tguser(tgid)
            current_photo = self.get_current_photo(message, only_hash=True)
            last_photo = self.get_last_photo(tgid)
            
            same_photo = current_photo['photo_hash'] == last_photo['photo_hash']
            
            if same_photo & current_photo['exists']:
                pass

            else:
                self.update_photo(message)
        except Exception as e:
            pass
        

        
        
        