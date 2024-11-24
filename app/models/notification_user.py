from app.models import db
from app.models.audit.base_audit import BaseAudit

class NotificationUser(BaseAudit):
    __tablename__ = 'notification_user'
    id = db.Column(db.Integer, primary_key = True)
    notification = db.Column(db.String(128), db.ForeignKey('notification.id'))
    user = db.Column(db.String(128), db.ForeignKey('user.id'))

    _notification = db.relationship('Notification', backref = db.backref('users'), lazy = True)
    _user = db.relationship('User', backref = db.backref('notifications'), lazy = True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "notification": self._notification.serialize(),
            "user": self._user.serialize()
        }