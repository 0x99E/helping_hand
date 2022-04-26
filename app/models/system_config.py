from email.policy import default
from . import base
db = base.db

class System(db.Model):
    __tablename__ = "system"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    session_timeout = db.Column(db.Integer(), default=60*60*24*7*2)
    
    def __repr__(self, ):
        return "<System %r, session_timeout=%r,>" % (self.id, self.session_timeout)

    def to_dict(self, ):
        return {
            "id": self.id,
            "session_timeout": self.session_timeout,
        }