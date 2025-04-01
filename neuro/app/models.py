from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class ShootingDate(db.Model):
    __tablename__ = 'shooting_dates'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    announcement_id = db.Column(db.Integer, db.ForeignKey('studio_announcement.id'))
    
    announcement = db.relationship('StudioAnnouncement', back_populates='dates')

class StudioAnnouncement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    button_text = db.Column(db.String(50), default="Записаться")
    
    # Связь с датами
    dates = db.relationship('ShootingDate', back_populates='announcement', cascade='all, delete-orphan')

class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Остальные модели без изменений

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    people_count = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    shooting_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(100))