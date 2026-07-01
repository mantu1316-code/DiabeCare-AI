import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import os


if os.path.exists('diabetes_2.csv'):
    print("🔄 Loading new dataset: diabetes_2.csv...")
    df = pd.read_csv('diabetes_2.csv')
elif os.path.exists('diabetes.csv'):
    print("🔄 Loading default dataset: diabetes.csv...")
    df = pd.read_csv('diabetes.csv')
else:
    raise FileNotFoundError("🚨 Error: Neither 'diabetes.csv' nor 'diabetes_2.csv' was found in the directory!")


cols_to_fix = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in cols_to_fix:
    df[col] = df[col].replace(0, df[col].median())


X = df.drop('Outcome', axis=1)
y = df['Outcome']


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)


model = RandomForestClassifier(
    n_estimators=500, 
    max_depth=15, 
    min_samples_leaf=1, 
    class_weight='balanced', 
    random_state=42
)
model.fit(X_train, y_train)


pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))

print("🎉 Model and Scaler Retrained & Saved Successfully!")