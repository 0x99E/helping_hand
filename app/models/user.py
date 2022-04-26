from email.policy import default
from . import base
db = base.db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    photo = db.Column(db.Text(), default="")
    mentor = db.Column(db.Boolean(), default=False)
    description = db.Column(db.Text(), default="")
    uuid = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self, ):
        return "<User(id='%s', name='%s', photo='%s', mentor='%s', uuid='%s', description='%s', )>" % (self.id, self.name, self.photo, self.mentor, self.uuid, self.description)
    
    def to_dict(self, ):
        return {
            "id": self.id,
            "name": self.name,
            "photo": self.photo,
            "mentor": self.mentor,
            "uuid": self.uuid,
            "description": self.description,
        }