from datetime import datetime
from flask_login import UserMixin
from taskapp import db, login_manager
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    firstTimeUser = db.Column(db.Boolean, nullable=False, default=True)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user.id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user.id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.firstTimeUser}')"

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return f"Goal('{self.title}', '{self.description}', '{self.date_created}', '{self.completed}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    goals = db.relationship('Goals', backref='task', lazy=True)
    
    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.date_created}','{self.deadline}', '{self.completed}')"     

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='project', lazy=True)
    
    @property
    def progress(self):
        if not self.tasks:
            return 0
        
        completed_task = 0 
        for task in self.tasks:
            if task.completed:
                completed_task += 1
        return (completed_task / len(self.tasks)) * 100


    def __repr__(self):
        return f"Project('{self.name}', '{self.description}', '{self.date_created}', '{self.deadline}', '{self.completed}, '{self.progress}')"