from sqlalchemy import DateTime, func
from app.models import db

class BaseAudit:
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    updated_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())
    active = db.Column(db.Boolean, default=True)
    
    #_created_by = db.relationship('User', backref = db.backref('audits'), lazy = True)
    #_updated_by = db.relationship('User', backref = db.backref('audits'), lazy = True)

    def serialize(self):
        return {
            "created_by": self._created_by.serialize(),
            "updated_by": self._updated_by.serialize(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "active": self.active
        }