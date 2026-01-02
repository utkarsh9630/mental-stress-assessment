from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd
import numpy as np
import joblib
import json
import json as json_module
import os
from models import db, User, Profile, Assessment
from forms import RegistrationForm, LoginForm, ProfileForm

app = Flask(__name__)
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///stress_assessment.db')

# Handle postgres:// to postgresql:// conversion for Render
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.template_filter('from_json')
def from_json_filter(s):
    return json_module.loads(s)
    
# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load ML models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.joblib"))
imputer = joblib.load(os.path.join(BASE_DIR, "models", "imputer.joblib"))
rf_model = joblib.load(os.path.join(BASE_DIR, "models", "rf_model.joblib"))
knn_model = joblib.load(os.path.join(BASE_DIR, "models", "knn_model.joblib"))

with open(os.path.join(BASE_DIR, "models", "label_map.json")) as f:
    label_map = json.load(f)
with open(os.path.join(BASE_DIR, "models", "feature_columns.json")) as f:
    feature_columns = json.load(f)
with open(os.path.join(BASE_DIR, "models", "rec_feature_columns.json")) as f:
    rec_feature_columns = json.load(f)

train_recs = pd.read_csv(os.path.join(BASE_DIR, "data", "train_recs.csv"))
train_recs["Mechanisms"] = train_recs["Stress Coping Mechanisms"].str.split(",")
inv_map = {int(k): v for k, v in label_map.items()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dashboard Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    profiles = Profile.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/dashboard.html', profiles=profiles)

@app.route('/profile/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile(
            user_id=current_user.id,
            profile_name=form.profile_name.data,
            age=form.age.data,
            gender=form.gender.data
        )
        db.session.add(profile)
        db.session.commit()
        flash('Profile created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard/create_profile.html', form=form)

@app.route('/profile/<int:profile_id>')
@login_required
def view_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    if profile.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    assessments = Assessment.query.filter_by(profile_id=profile_id).order_by(Assessment.created_at.desc()).all()
    return render_template('dashboard/profile.html', profile=profile, assessments=assessments)

@app.route('/profile/<int:profile_id>/assess')
@login_required
def assess_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    if profile.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('assess.html', profile=profile)

@app.route('/profile/<int:profile_id>/delete', methods=['POST'])
@login_required
def delete_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    if profile.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(profile)
    db.session.commit()
    flash('Profile deleted successfully', 'success')
    return redirect(url_for('dashboard'))

# Assessment Routes
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.json
        profile_id = data.get('profile_id')
        
        # Build input
        input_dict = {
            'Age': float(data['age']),
            'Academic Performance (GPA)': float(data['gpa']),
            'Study Hours Per Week': float(data['study_hours']),
            'Social_Media_Usage_per_week': float(data['social_media']) * 7,
            'Sleep Duration (Hours per night)': float(data['sleep']),
            'Physical Exercise (Hours per week)': float(data['exercise']),
            'Family Support': int(data['family_support']),
            'Financial Stress': int(data['financial_stress']),
            'Peer Pressure': int(data['peer_pressure']),
            'Relationship Stress': int(data['relationship_stress']),
            'Counseling Attendance': 1 if data['counseling'] == 'Yes' else 0,
            'Diet Quality': int(data['diet_quality']),
            'Cognitive Distortions': int(data['cognitive_distortions']),
            'Family Mental Health History': 1 if data['family_mental_history'] == 'Yes' else 0,
            'Medical Condition': 1 if data['medical_condition'] == 'Yes' else 0,
            'Substance Use': int(data['substance_use']),
            'Gender_Female': 1 if data['gender'] == 'Female' else 0,
            'Gender_Male': 1 if data['gender'] == 'Male' else 0,
            'Gender_Other': 1 if data['gender'] == 'Other' else 0
        }
        
        numerator = (input_dict['Financial Stress'] + input_dict['Peer Pressure'] + input_dict['Relationship Stress'])
        denominator = (input_dict['Family Support'] + input_dict['Diet Quality'] + input_dict['Physical Exercise (Hours per week)'])
        if denominator == 0:
            denominator = 0.001
        input_dict['Stress_Ratio'] = numerator / denominator
        
        X_df = pd.DataFrame([input_dict])[feature_columns]
        X_imp = imputer.transform(X_df.values)
        X_scaled = scaler.transform(X_imp)
        probs = rf_model.predict_proba(X_scaled)[0]
        pred_int = int(probs.argmax())
        pred_label = inv_map[pred_int]
        
        current_mechanisms = data.get('current_mechanisms', [])
        recommendations = get_recommendations(input_dict, pred_int, probs, current_mechanisms)
        
        if pred_int == 2:
            p_drop = float(probs[0] + probs[1])
        elif pred_int == 1:
            p_drop = float(probs[0])
        else:
            p_drop = 0.0
        
        # Save assessment to database
        if profile_id:
            assessment = Assessment(
                profile_id=profile_id,
                age=data['age'],
                gender=data['gender'],
                gpa=data['gpa'],
                study_hours=data['study_hours'],
                social_media=data['social_media'],
                sleep=data['sleep'],
                exercise=data['exercise'],
                family_support=data['family_support'],
                financial_stress=data['financial_stress'],
                peer_pressure=data['peer_pressure'],
                relationship_stress=data['relationship_stress'],
                counseling=data['counseling'],
                diet_quality=data['diet_quality'],
                cognitive_distortions=data['cognitive_distortions'],
                family_mental_history=data['family_mental_history'],
                medical_condition=data['medical_condition'],
                substance_use=data['substance_use'],
                current_mechanisms=json.dumps(current_mechanisms),
                predicted_stress=pred_label,
                prob_low=float(probs[0]),
                prob_medium=float(probs[1]),
                prob_high=float(probs[2]),
                drop_probability=p_drop,
                recommendations=json.dumps(recommendations)
            )
            db.session.add(assessment)
            db.session.commit()
        
        return jsonify({
            'prediction': pred_label,
            'probabilities': {
                'Low': float(probs[0]),
                'Medium': float(probs[1]),
                'High': float(probs[2])
            },
            'drop_probability': p_drop,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def get_recommendations(input_dict, pred_int, probs, current_mechanisms, k=50, m=5):
    X_rec = pd.DataFrame([input_dict])[rec_feature_columns].values.reshape(1, -1)
    _, idxs = knn_model.kneighbors(X_rec, n_neighbors=k)
    neighbors = train_recs.iloc[idxs[0]]
    
    stats = {}
    for mechs, stress_level in zip(neighbors["Mechanisms"], neighbors["Stress Level Category"]):
        success = 1 if stress_level == "Low" else 0
        for mech in mechs:
            mech = mech.strip()
            if mech not in stats:
                stats[mech] = {"used": 0, "success": 0}
            stats[mech]["used"] += 1
            stats[mech]["success"] += success
    
    mech_list = []
    for mech, v in stats.items():
        if v["used"] > 0:
            mech_list.append({"mechanism": mech, "success_rate": v["success"] / v["used"]})
    
    current_set = set(m.strip() for m in current_mechanisms)
    mech_list = [m for m in mech_list if m["mechanism"] not in current_set]
    mech_list.sort(key=lambda x: x["success_rate"], reverse=True)
    return mech_list[:m]

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})
    
@app.route('/init-db')
def init_database():
    """Initialize database tables - remove this endpoint after first use"""
    try:
        db.create_all()
        return jsonify({
            'status': 'success',
            'message': 'Database tables created successfully!',
            'tables': ['stress_users', 'stress_profiles', 'stress_assessments']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)