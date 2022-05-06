from email.policy import default
from pydoc import describe
from . import base
db = base.db

class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), default="")
    answer = db.Column(db.Text(), default="")
    closed = db.Column(db.Boolean(), default=False)
    student = db.Column(db.Text(), nullable=False)
    mentor = db.Column(db.Text(), default="")
    uuid = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.String(), default="")
    idate = db.Column(db.Integer(), default=0)

    def __repr__(self, ):
        return "<Task(id='%s', name='%s', description='%s', answer='%s', closed='%s', student='%s', mentor='%s', uuid='%s', date='%s', idate='%s',)>" % (
            self.id, 
            self.name, 
            self.description, 
            self.answer, 
            self.closed, 
            self.student,
            self.mentor, 
            self.uuid,
            self.date,
            self.idate,
            )
    
    def to_dict(self, ):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "answer": self.answer,
            "closed": self.closed,
            "student": self.student,
            "mentor": self.mentor,
            "uuid": self.uuid,
            "date": self.date,
            "idate": self.idate,
        }