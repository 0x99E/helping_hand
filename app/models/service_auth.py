from pydoc import describe
from . import base
db = base.db

class SERVICEAuth(db.Model):
    __tablename__ = "service_auth"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), )
    token = db.Column(db.Text(), )

    
    def __repr__(self, ):
        return f"<SERVICEAuth({self.to_dict()})>"

    def to_dict(self, ):
        return {
            "id": self.id,
            "name": self.name,
            "token": self.token,
            }