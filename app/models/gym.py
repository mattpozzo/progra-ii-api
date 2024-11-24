from . import db

# Clase Gym
class Gym(db.Model):
    __tablename__ = "gym"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }