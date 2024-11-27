from flask import request
from flask_restx import Namespace, Resource

from app.models import db
from app.models.models import User
from app.resources.auth.authorize import authorize

notification_ns = Namespace('notifications', description='Operaciones relacionadas con las notificaciones')

@notification_ns.route('/')
class GetNotifications(Resource):
    @authorize
    def get(user: User, self):
        # Create filter condition
        read = request.args.get('read', type=lambda x: x.lower() == 'true')
        cond = lambda x: (x.read == read) if read is not None else True

        notifications = [notification for notification in user.notifications if cond(notification)]
        returned_notifications = [notification.serialize() for notification in notifications]

        # Mark returned notifications as read
        [notification.read_notification() for notification in notifications]
        db.session.commit()

        return returned_notifications, 200

@notification_ns.route('/<int:id>')
class GetNotification(Resource):
    @authorize
    def get(user: User, self, id):
        notification = next((notification for notification in user.notifications if notification.notification.id == id), None)
        if notification:
            returned_notification = notification.serialize()

            # Mark notification as read
            notification.read_notification()
            db.session.commit()

            return returned_notification, 200
        else:
            return {'message': 'Notification not found.'}, 404

@notification_ns.route('/unread')
class UnreadNotifications(Resource):
    @authorize
    def post(user: User, self):
        notification_ids = request.json.get('notifications')

        if not notification_ids:
            return {'message': 'Missing required notifications field.'}, 400

        notifications = [notification for notification in user.notifications if notification.notification.id in notification_ids]

        if len(notifications) != len(notification_ids):
            return {'message': 'Some notifications do not exist.'}, 404

        [notification.unread_notification() for notification in notifications]
        db.session.commit()

        return [notification.serialize() for notification in notifications], 200