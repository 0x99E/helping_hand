import random
import config
import os
import base64
import message_template

class Handler():
    def __init__(self, bot=None, api=None):
        self.bot = bot
        self.api = api
    
    def random_str(self, size=10):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(size))

    def user_hander(self, message):
        tgid = message.from_user.id
        uuid = None

        tg_user_exists = None

        tg_user_exists = self.api.tguser_exists(tgid)

        if tg_user_exists:
            tguser = self.api.get_tguser(tgid)
            uuid = tguser["uuid"]
            user = self.api.get_user(uuid)
        else:
            user = self.create_user(message)

        return user

    def cmd_handler(self, message):
        text = message.text
        tguser = self.parse_user(message, no_photo=True)
        chat_id = message.chat.id
        reply = ""
        if text == "/start":
            name = tguser["first_name"]
            token = "12345678910"
            link = config.web_url + "auth/" + token
            reply = message_template.default
            reply = reply.format(name=name, link=link, token=token)
            self.bot.send_message(chat_id, reply, parse_mode="HTML")
        else:
            name = tguser["first_name"]
            token = "12345678910"
            link = config.web_url + "auth/" + token
            reply = message_template.default
            reply = reply.format(name=name, link=link, token=token)
            self.bot.send_message(chat_id, reply, parse_mode="HTML")

    def handle(self, message):
        self.user_hander(message)
        self.cmd_handler(message)
        
    def create_user(self, message):
        parameters = {}
        parameters = self.parse_user(message)
        user = self.api.create_user(parameters)
        return user

    def parse_user(self, message, no_photo=False):
        result = {}
        result["first_name"] = message.from_user.first_name
        result["last_name"] = message.from_user.last_name
        result["username"] = message.from_user.username
        result["mentor"] = False
        result["tgid"] = message.from_user.id
        result["photo"] = ""
        result["photo_hash"] = ""
        if not no_photo:
            user_photo = self.get_tg_user_photo(message)
            result["photo"] = user_photo["photo"]
            result["photo_hash"] = user_photo["photo_hash"]
        result["known_photo"] = ""

        return result

    def get_tg_user_photo(self, message):
        result = {}
        tgid = message.from_user.id
        user_photos = self.bot.get_user_profile_photos(tgid)
        photo = user_photos.photos[0][0]

        photo_id = photo.file_id
        photo_hash = photo.file_unique_id

        photo_file = self.bot.get_file(photo_id)
        photo_file_path = photo_file.file_path

        bphoto = self.bot.download_file(file_path=photo_file_path)
        random_name = self.random_str() + ".jpg"
        # Create full path to photo
        bbasephoto = base64.b64encode(bphoto)
        bbasephoto = bbasephoto.decode("utf-8")
        bbasephoto = "data:image/png;base64," + bbasephoto 
        result["photo"] = bbasephoto
        result["photo_hash"] = photo_hash
        return result
        
        
        