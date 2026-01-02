from app import app, db
from models import User, Profile, Assessment

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    print("Tables created:")
    print("- stress_users")
    print("- stress_profiles")
    print("- stress_assessments")