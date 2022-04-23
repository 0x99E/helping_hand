from . import base
db = base.db

class TGUser(db.Model):
    __tablename__ = "tguser"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text(), )
    last_name = db.Column(db.Text(), )
    username = db.Column(db.Text(), )
    photo = db.Column(db.Text(), )
    photo_hash = db.Column(db.Text(), )
    known_photo = db.Column(db.Text(), )
    created_at = db.Column(db.Text(), )
    tgid = db.Column(db.String(100), unique=True, nullable=False)
    uuid = db.Column(db.String(100), unique=True)

    def __repr__(self, ):
        return "<TGUser(id='%s', first_name='%s', last_name='%s', username='%s', photo='%s', photo_hash='%s', known_hash='%s', created_at='%s', uuid='%s')>" % (self.id, self.first_name, self.last_name, self.username, self.photo, self.photo_hash, self.known_photo, self.created_at, self.uuid)

    def to_dict(self, ):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "photo": self.photo,
            "photo_hash": self.photo_hash,
            "known_photo": self.known_photo,
            "created_at": self.created_at,
            "tgid": self.tgid,
            "uuid": self.uuid,
        }