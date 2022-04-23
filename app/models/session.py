from . import base
db = base.db

class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uuid = db.Column(db.Text(), )
    session_token = db.Column(db.Text(), )
    
    def __repr__(self, ):
        return "<Session(id='%s', uuid='%s', session_token='%s')>" % (self.id, self.uuid, self.session_token)
    
    def to_dict(self, ):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "session_token": self.session_token,
        }