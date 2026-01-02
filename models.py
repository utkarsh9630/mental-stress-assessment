from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profiles = db.relationship('Profile', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='profile', lazy=True, cascade='all, delete-orphan')

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    
    # Input data
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    gpa = db.Column(db.Float)
    study_hours = db.Column(db.Float)
    social_media = db.Column(db.Float)
    sleep = db.Column(db.Float)
    exercise = db.Column(db.Float)
    family_support = db.Column(db.Integer)
    financial_stress = db.Column(db.Integer)
    peer_pressure = db.Column(db.Integer)
    relationship_stress = db.Column(db.Integer)
    counseling = db.Column(db.String(10))
    diet_quality = db.Column(db.Integer)
    cognitive_distortions = db.Column(db.Integer)
    family_mental_history = db.Column(db.String(10))
    medical_condition = db.Column(db.String(10))
    substance_use = db.Column(db.Integer)
    current_mechanisms = db.Column(db.Text)  # JSON string
    
    # Results
    predicted_stress = db.Column(db.String(20))
    prob_low = db.Column(db.Float)
    prob_medium = db.Column(db.Float)
    prob_high = db.Column(db.Float)
    drop_probability = db.Column(db.Float)
    recommendations = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)