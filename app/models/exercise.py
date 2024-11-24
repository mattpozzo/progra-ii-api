from app.models import db

class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False, unique=True)
    description = db.Column(db.String(512))
    muscle = db.Column(db.String(128), db.ForeignKey('muscle.id')) #Esto es foreign key a tabla muscle group 

    _muscle = db.relationship('Muscle', backref = db.backref('exercises'), lazy = True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "muscle": self._muscle.serialize()
        }