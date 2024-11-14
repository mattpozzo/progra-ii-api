from app.models import db

class Muscle(db.Model):
    __tablename__ = 'muscle'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False, unique=True)
    description = db.Column(db.String(512))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        } 




