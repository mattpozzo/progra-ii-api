from flask_restx import Namespace, Resource
from app.models.notification import Notification

from app.models.user import User
from app.resources.auth.authorize import authorize

notification_ns = Namespace('notifications', description='Operaciones relacionadas con las notificaciones')

@notification_ns.route('/')
class GetNotifications(Resource):
    @authorize
    def get(user: User, self):  # asco but ok?
        return [notification.serialize() for notification in user.notifications], 200
