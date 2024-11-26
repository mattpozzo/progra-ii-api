from app.models import db
from app.models.audit.base_audit import BaseAudit

notification_user = db.Table('notification_user',
    db.Column('notification', db.Integer, db.ForeignKey('notification.id')),
    db.Column('user', db.Integer, db.ForeignKey('user.id'))
)