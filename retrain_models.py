import pandas as pd
import numpy as np
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

print("Loading data...")
df = pd.read_csv("Mental_Stress_and_Coping_Mechanisms_processed_final.csv")

# Reconstruct target from dummies
dummy_cols = [
    "Stress Level Category_Low",
    "Stress Level Category_Medium",
    "Stress Level Category_High"
]
df['Stress Level Category'] = (
    df[dummy_cols]
      .idxmax(axis=1)
      .str.replace("Stress Level Category_", "", regex=False)
)

cols_to_drop = [
    "Mental Stress Level",
    *dummy_cols,
    "Stress Coping Mechanisms",
    "Unnamed: 0",
    "Student_id"
]
df = df.drop(columns=cols_to_drop, errors="ignore")

# Combine less common genders
df['Gender_Other'] = (df[['Gender_Agender','Gender_Bigender','Gender_Genderfluid']].sum(axis=1).clip(upper=1))

# Convert social media usage
df['Social_Media_Usage_per_week'] = df['Social Media Usage (Hours per day)'] * 7

# Calculate Stress_Ratio
df['Stress_Ratio'] = (
    (df['Financial Stress'] + df['Peer Pressure'] + df['Relationship Stress']) /
    (df['Family Support'] + df['Diet Quality'] + df['Physical Exercise (Hours per week)'] + 0.001)
)

# Select features
selected_features = [
    'Age','Academic Performance (GPA)','Study Hours Per Week',
    'Social_Media_Usage_per_week','Sleep Duration (Hours per night)',
    'Physical Exercise (Hours per week)','Family Support','Financial Stress',
    'Peer Pressure','Relationship Stress','Counseling Attendance','Diet Quality',
    'Cognitive Distortions','Family Mental Health History','Medical Condition',
    'Substance Use','Gender_Female','Gender_Male','Gender_Other','Stress_Ratio'
]

X = df[selected_features]
y = df['Stress Level Category']

# Remove outliers
Q1, Q3 = X['Study Hours Per Week'].quantile([0.25,0.75])
IQR = Q3 - Q1
mask = X['Study Hours Per Week'].between(Q1-1.5*IQR, Q3+1.5*IQR)
X, y = X[mask], y[mask]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

print("Training models...")

# Train imputer
imputer = SimpleImputer(strategy='mean')
X_train_imp = imputer.fit_transform(X_train)

# Train scaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imp)

# Train Random Forest
label_map = {'Low': 0, 'Medium': 1, 'High': 2}
y_train_encoded = y_train.map(label_map)

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train_encoded)

# Train k-NN for recommendations
rec_features = selected_features.copy()
knn_model = NearestNeighbors(n_neighbors=50, metric="euclidean")
knn_model.fit(X_train_scaled)

print("Saving models...")

# Save all artifacts
joblib.dump(scaler, "models/scaler.joblib")
joblib.dump(imputer, "models/imputer.joblib")
joblib.dump(rf_model, "models/rf_model.joblib")
joblib.dump(knn_model, "models/knn_model.joblib")

# Save feature columns
with open("models/feature_columns.json", "w") as f:
    json.dump(selected_features, f)

with open("models/rec_feature_columns.json", "w") as f:
    json.dump(rec_features, f)

# Save label map
with open("models/label_map.json", "w") as f:
    json.dump({"0": "Low", "1": "Medium", "2": "High"}, f)

print("Done! Models retrained and saved.")
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")