from . import base
db = base.db

class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uuid = db.Column(db.Text(), )
    token = db.Column(db.Text(), )
    
    def __repr__(self, ):
        return f"<Auth({self.to_dict()})>"
    
    def to_dict(self, ):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "token": self.token,
        }