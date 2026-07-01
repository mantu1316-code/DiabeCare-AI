import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(page_title="DiabeCare AI - Professional", layout="wide", page_icon="🩺")

# Load model and scaler
@st.cache_resource
def load_resources():
    try:
        model = pickle.load(open('model.pkl', 'rb'))
        scaler = pickle.load(open('scaler.pkl', 'rb'))
        return model, scaler
    except:
        return None, None

model, scaler = load_resources()

# --- FIXED CSS FOR VISIBILITY ---
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #f8f9fa; }
    
    /* Force all text to be dark/visible */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Button styling */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background: linear-gradient(90deg, #007bff, #0056b3); 
        color: white !important; font-weight: bold; border: none;
    }
    
    /* Precaution cards with dark text */
    .report-card { 
        padding: 15px; border-radius: 10px; background-color: #ffffff; 
        border-left: 5px solid #007bff; margin-bottom: 10px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        color: #1a1a1a !important;
    }
    
    /* Sidebar text color */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: #1a1a1a !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 Advanced Diabetes Diagnostic System")
st.write("Clinical analysis based on PIMA Dataset and Medical Research Standards.")
st.markdown("---")

if model is None:
    st.error("🚨 'model.pkl' ya 'scaler.pkl' nahi mila. Pehle 'train.py' run karein.")
else:
    # Sidebar Profile
    with st.sidebar:
        st.header("👤 Patient Profile")
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        age = st.slider("Age", 1, 120, 30)
        dpf = st.number_input("Diabetes Pedigree Function (DPF)", 0.0, 3.0, 0.47)
        st.info("DPF: Genetic risk score based on family history.")

    # Main Input Columns
    col1, col2 = st.columns(2)
    with col1:
        glu = st.number_input("Glucose Level (mg/dL)", 0, 300, 100)
        bp = st.number_input("Blood Pressure (mm Hg)", 0, 150, 80)
        preg = st.number_input("Pregnancies", 0, 20, 0) if gender == "Female" else 0
        if gender == "Male": st.caption("Pregnancies: N/A for Male")

    with col2:
        bmi = st.number_input("BMI (Body Mass Index)", 0.0, 70.0, 25.0)
        ins = st.number_input("Insulin Level (mu U/ml)", 0, 900, 80)
        skin = st.number_input("Skin Thickness (mm)", 0, 100, 20)

    st.markdown("---")

    if st.button("Generate Detailed Medical Report"):
        # Prediction
        input_data = np.array([[preg, glu, bp, skin, ins, bmi, dpf, age]])
        input_scaled = scaler.transform(input_data)
        prob = model.predict_proba(input_scaled)[0][1] * 100
        
        # Clinical Rule Override
        if glu >= 150 or (glu >= 130 and bmi >= 33):
            if prob < 75: prob = 85.0

        # Risk Logic
        if prob < 30:
            status, color = "LOW RISK", "#28a745"
            precautions = [
                "Daily 30 minutes brisk walking ya yoga maintain karein.",
                "High-fiber diet (fruits, vegetables, oats) ko badhawa dein.",
                "Meethi cold-drinks aur processed snacks se parhez karein.",
                "Apna ideal body weight (BMI 18-25) maintain karne ki koshish karein.",
                "Health monitoring ke liye saal mein ek baar checkup karwayein."
            ]
        elif 30 <= prob < 70:
            status, color = "MEDIUM RISK (PREDIABETIC)", "#fd7e14"
            precautions = [
                "Refined carbs (White bread, Maida) aur Sugar turant kam karein.",
                "Din mein kam se kam 45 minutes active rahein (Cardio/Cycling).",
                "Har 3-6 mahine mein HbA1c test karwa kar trend check karein.",
                "Meal portion control karein aur raat ka khana sone se 3 ghante pehle khayein.",
                "Doctor ya Dietitian se mil kar personalized diet plan banwayein."
            ]
        else:
            status, color = "HIGH RISK (DIABETIC)", "#dc3545"
            precautions = [
                "Turant kisi Specialist Physician ya Endocrinologist se milein.",
                "Fasting aur Khane ke baad (PP) sugar levels ki daily monitoring karein.",
                "Prescribed medicines ya Insulin dosage ko bina miss kiye follow karein.",
                "Sugar, Sweets aur High-Glycemic fruits (Aam, Kela) bilkul band karein.",
                "Ankhon, Daanto aur Pairon (Feet) ka vishesh dhyan rakhein (Diabetic care)."
            ]

        # Charts Section
        vcol1, vcol2 = st.columns(2)
        
        with vcol1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob,
                number = {'suffix': "%", 'font': {'size': 50, 'color': '#1a1a1a'}},
                title = {'text': f"Diagnosis: {status}", 'font': {'size': 20, 'color': color}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "#1a1a1a"},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 30], 'color': "#e8f5e9"},
                        {'range': [30, 70], 'color': "#fff3e0"},
                        {'range': [70, 100], 'color': "#ffebee"}]
                }
            ))
            fig_gauge.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font={'color': "#1a1a1a"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        with vcol2:
            factors = ['Glucose', 'BMI', 'Age', 'BP', 'Insulin']
            scores = [glu/2.5, bmi, age, bp/1.2, ins/10]
            fig_bar = go.Figure(go.Bar(
                x=scores, y=factors, orientation='h', marker_color=color,
                text=[f"{s:.0f}" for s in scores], textposition='auto'
            ))
            fig_bar.update_layout(title="Risk Contribution Factors", height=350, yaxis_autorange="reversed", paper_bgcolor='rgba(0,0,0,0)', font={'color': "#1a1a1a"})
            st.plotly_chart(fig_bar, use_container_width=True)

        # Report Summary
        st.markdown(f"### 📋 Personal Recommendations for {status}")
        rep_col1, rep_col2 = st.columns(2)
        with rep_col1:
            for p in precautions:
                st.markdown(f"<div class='report-card' style='border-left-color:{color};'>• {p}</div>", unsafe_allow_html=True)
        with rep_col2:
            st.subheader("Vital Analysis Summary")
            st.write(f"🩺 **Glucose:** {'High' if glu > 125 else 'Elevated' if glu > 100 else 'Normal'}")
            st.write(f"⚖️ **BMI:** {'Obese' if bmi >= 30 else 'Overweight' if bmi >= 25 else 'Healthy'}")
            st.write(f"🎂 **Age Risk:** {'High' if age > 45 else 'Moderate'}")

    st.markdown("---")
    st.caption("Note: This report is for informational purposes only. Consult a doctor for medical diagnosis.")