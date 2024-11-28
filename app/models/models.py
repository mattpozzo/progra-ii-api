from typing import List

from sqlalchemy import DateTime, Time
from app.models import db
from app.models.audit.base_audit import BaseAudit
from sqlalchemy.orm import Mapped

from werkzeug.security import generate_password_hash, check_password_hash
import os


class Comment(db.Model, BaseAudit):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    body = db.Column(db.String(), nullable=False)

    post = db.relationship('Post', backref=db.backref('comments'), lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "post": self.post.serialize(),
            "comment": self.comment.serialize(),
            "body": self.body
        }


Comment.comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
Comment.comment = db.relationship('Comment',
                                  backref=db.backref('comments'),
                                  lazy=True,
                                  remote_side=Comment.id)


class Exercise(db.Model, BaseAudit):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512))
    muscle_id = db.Column(db.Integer,
                          db.ForeignKey('muscle.id'),
                          nullable=False)

    muscle = db.relationship('Muscle',
                             backref=db.backref('exercises'),
                             lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "muscle": self.muscle.serialize()
        }

# Muscle.exercises abajo de Muscle


class Gym(db.Model, BaseAudit):
    __tablename__ = "gym"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class MealSchedule(db.Model):
    __tablename__ = 'meal_schedule'

    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Time, nullable=False)
    training_plan_id = db.Column(db.Integer, nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'),
                          nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('meal_schedules',
                                                          lazy=True))


class Muscle(db.Model, BaseAudit):
    __tablename__ = 'muscle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


# Muscle.exercises = db.relationship('Exercise', back_populates="muscle", foreign_keys=[Exercise.id])


class Notification(db.Model, BaseAudit):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), nullable = False)
    body = db.Column(db.String(512), nullable = False)

    users: Mapped[List['NotificationUser']] = db.relationship(back_populates = 'notification', lazy = True)

    # Envía la notificación a un conjunto de usuarios, TODO: ver si funciona
    def send_to_users(self, users):
        for user in users:
            notification_user = NotificationUser(user = user, notification = self)
            db.session.add(notification_user)
        db.session.commit()

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "title": self.title,
            "body": self.body,
        }


class NotificationUser(BaseAudit, db.Model):
    __tablename__ = "notification_user"
    notification_id = db.Column(db.ForeignKey("notification.id"), primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    read = db.Column(db.Boolean, default=False)

    user: Mapped['User'] = db.relationship(back_populates="notifications", foreign_keys=[user_id])
    notification: Mapped['Notification'] = db.relationship(back_populates="users", foreign_keys=[notification_id])

    def serialize(self):
        return super().serialize() | {
            "notification": self.notification.serialize(),
            "read": self.read
        }

    def read_notification(self):
        self.read = True
        return self

    def unread_notification(self):
        self.read = False
        return self


class Post(db.Model, BaseAudit):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'))
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(), nullable=False)

    gym = db.relationship('Gym', backref=db.backref('posts'), lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "gym": self.gym.serialize(),
            "title": self.title,
            "body": self.body
        }


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    author = db.Column(db.Integer, nullable=True)  # FALTA ForeignKey


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey('recipe.id'),
                          nullable=False)
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredient.id'),
                              nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('ingredients',
                                                          lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipes',
                                                                  lazy=True))
    


class Review(db.Model):
    __tablename__ = 'review'

    UniqueID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=True)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=True)

    # Relación con Recipe
    recipe = db.relationship('Recipe', backref='reviews', lazy=True)

    # Relación con Gym (si es necesario)
    gym = db.relationship('Gym', backref='reviews', lazy=True)


    def serialize(self):
        return super().serialize() | {
            'UniqueID': self.UniqueID,
            'score': self.score,
            'comment': self.comment,
            'recipe_id': self.recipe_id,
            'gym_id': self.gym_id,
            'recipe': self.recipe.serialize() if self.recipe else None,  # Suponiendo que Recipe tenga su propio método serialize
            'gym': self.gym.serialize() if self.gym else None  # Suponiendo que Gym tenga su propio método serialize
        }


class Request(db.Model, BaseAudit):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    request_status_id = db.Column(db.Integer,
                                  db.ForeignKey('request_status.id'))
    request_type_id = db.Column(db.Integer, db.ForeignKey('request_type.id'))
    body = db.Column(db.String(), nullable=False)

    request_status = db.relationship('RequestStatus',
                                     backref=db.backref('requests'),
                                     lazy=True)
    request_type = db.relationship('RequestType',
                                   backref=db.backref('requests'),
                                   lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "request_status": self.request_status.serialize(),
            "request_type": self.request_type.serialize(),
            "body": self.body
        }


class RequestReceiver(db.Model, BaseAudit):
    __tablename__ = 'request_receiver'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))

    user = db.relationship('User',
                           backref=db.backref('requests'),
                           lazy=True,
                           foreign_keys=[user_id])
    request = db.relationship('Request',
                              backref=db.backref('receivers'),
                              lazy=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "user": self.user.serialize(),
            "request": self.request.serialize(),
        }


class RequestStatus(db.Model, BaseAudit):
    __tablename__ = 'request_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
        }


class RequestType(db.Model, BaseAudit):
    __tablename__ = 'request_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    body_template = db.Column(db.String(), nullable=False)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "body_template": self.body_template,
        }


class Routine(db.Model, BaseAudit):
    __tablename__ = 'routine'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128),
                     nullable=False,
                     unique=True)
    description = db.Column(db.String(512))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'))

    user = db.relationship('User',
                           backref=db.backref('routines',
                                              lazy=True),
                           foreign_keys=[user_id])
    gym = db.relationship('Gym',
                          backref=db.backref('routines',
                                             lazy=True))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'name': self.name,
            'description': self.description,  # Guarda si es Null,
                                              # podría ser None, PROBAR
            'user': self.user.serialize(),
            'gym': self.gym.serialize() if self.gym else None
        }


class RoutineExercise(db.Model, BaseAudit):
    __tablename__ = 'routine_exercise'
    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    notes = db.Column(db.String(512))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),
                           nullable=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))

    exercise = db.relationship('Exercise',
                               backref=db.backref('routine_exercises',
                                                  lazy=True),
                               foreign_keys=[exercise_id])
    session = db.relationship('Session',
                              backref=db.backref('routine_exercise',
                                                 lazy=True),
                              foreign_keys=[session_id])
    routine = db.relationship('Routine',
                              back_populates='routine_exercises',
                              foreign_keys=[routine_id])

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'sets': self.sets,
            'reps': self.reps,
            'weight': self.weight,
            'exercise': self.exercise.serialize(),
            'session': self.session.serialize() if self.session else None,
            'routine': self.routine.serialize()
        }


Routine.routine_exercises: Mapped[List['RoutineExercise']] = db.relationship('RoutineExercise',
                                              back_populates='routine',
                                              foreign_keys=[RoutineExercise.routine_id])


class RoutineSchedule(db.Model, BaseAudit):
    __tablename__ = 'routine_schedule'
    id = db.Column(db.Integer, primary_key=True)

    weekday = db.Column(db.Integer, nullable=False)
    hour = db.Column(Time, nullable=False)

    training_plan_id = db.Column(db.Integer, db.ForeignKey('training_plan.id'),
                                 nullable=False)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'),
                           nullable=False)

    training_plan = db.relationship('TrainingPlan',
                                    backref=db.backref('routine_schedules',
                                                       lazy=True))
    routine = db.relationship('Routine')

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'weekday': self.weekday,
            'hour': self.hour,
            'training_plan': self.training_plan.serialize(),
            'routine': self.routine.serialize()
        }


class Session(db.Model, BaseAudit):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(DateTime(timezone=True), nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('sessions', lazy=True),
                           foreign_keys=[user_id])

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "date": self.date,
            "duration": self.duration,
            'user': self.user.serialize()
        }


class TrainingPlan(db.Model, BaseAudit):
    __tablename__ = 'training_plan'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    completed_week = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User',
                           backref=db.backref('training_plans',
                                              lazy=True),
                           foreign_keys=[user_id])

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            'name': self.name,
            'description': self.description,
            'user': self.user.serialize(),
            'completed_week': self.completed_week
        }


class Trophy(db.Model, BaseAudit):
    __tablename__ = 'trophy'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=False)

    # Entrega el trofeo a un usuario, TODO: ver si funciona
    def grant(self, user):
        user_trophy = UserTrophy(user=user, trophy=self)
        db.session.add(user_trophy)
        db.session.commit()

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    certified = db.Column(db.Boolean, nullable=False)

    notifications: Mapped[List['NotificationUser']] = db.relationship(back_populates="user", foreign_keys=[NotificationUser.user_id])

    def set_password(self, password):
        self.salt = os.urandom(16).hex()
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.salt)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "certified": self.certified,


            # "notifications": [notification.serialize() for notification in
            #                   self.notifications]

        }


class UserTrophy(db.Model, BaseAudit):
    __tablename__ = 'user_trophy'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    trophy_id = db.Column(db.ForeignKey('trophy.id'), primary_key=True)

    user: Mapped['User'] = db.relationship(back_populates='trophies',
                           foreign_keys=[user_id])
    trophy: Mapped['Trophy'] = db.relationship(back_populates='users',
                             foreign_keys=[trophy_id])

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "trophy": self.trophy.serialize(),
            "user": self.user.serialize()
        }

Trophy.users = db.relationship('UserTrophy', back_populates='trophy', foreign_keys=[UserTrophy.trophy_id])
User.trophies = db.relationship('UserTrophy', back_populates='user', foreign_keys=[UserTrophy.user_id])


class UserType(db.Model, BaseAudit):
    __tablename__ = "usertype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "name": self.name
        }

class UserTypeGym(db.Model, BaseAudit):
    # OPINION: habría que sacar el id y hacer que las tres FK sean la PK compuesta,
    # como en las otras tablas intermedias.
    __tablename__ = "usertypegym"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)
    user_type_id = db.Column(db.Integer,
                             db.ForeignKey('usertype.id'),
                             nullable=False)

    user: Mapped['User'] = db.relationship(back_populates="gyms", foreign_keys=[user_id])
    user_type = db.relationship('UserType',
                                backref=db.backref('user_type_gyms',
                                                   lazy=True))

    def serialize(self):
        return super().serialize() | {
            "id": self.id,
            "user": self.user.serialize(),
            "gym": self.gym.serialize(),
            "user_type": self.user_type.serialize()
        }
    
Gym.users = db.relationship('UserTypeGym', back_populates="gym", foreign_keys=[UserTypeGym.gym_id])    # I hate Python
User.gyms = db.relationship('UserTypeGym', back_populates="user", foreign_keys=[UserTypeGym.user_id])
UserTypeGym.gym = db.relationship('Gym', back_populates="users", foreign_keys=[UserTypeGym.gym_id])