from sqlalchemy import DateTime, func
from app.models import db
from sqlalchemy.ext.declarative import declared_attr

class BaseAudit:
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    updated_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())
    active = db.Column(db.Boolean, default=True)
    
    @declared_attr
    def _created_by(cls):
        return db.relationship('User', foreign_keys=[cls.created_by], lazy = True)
    
    @declared_attr
    def _updated_by(cls):
        return db.relationship('User', foreign_keys=[cls.updated_by], lazy = True)

    def serialize(self):
        return {
            "created_by": self._created_by.serialize() if self._created_by else None,
            "updated_by": self._updated_by.serialize() if self._updated_by else None,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "active": self.active
        }