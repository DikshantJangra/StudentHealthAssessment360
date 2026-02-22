import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="StudentHealth360", page_icon="⚕️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #ffffff; }
    
    .main .block-container { padding: 3rem 4rem; max-width: 1200px; }
    
    .header { text-align: center; margin-bottom: 3rem; }
    
    .main-title { font-size: 2.5rem; font-weight: 600; color: #000 !important; margin: 0; }
    
    .subtitle { font-size: 0.95rem; color: #6b7280; margin-top: 0.5rem; font-weight: 400; }
    
    .section-title { font-size: 0.85rem; font-weight: 600; color: #374151; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .stNumberInput label, .stSlider label, .stSelectbox label { color: #374151 !important; font-weight: 400 !important; font-size: 0.9rem !important; }
    
    .stNumberInput input, .stSelectbox select { border: 1px solid #e5e7eb !important; border-radius: 6px !important; }
    
    .stButton>button { background: #111827; color: white; font-weight: 500; border: none; padding: 0.75rem 2rem; border-radius: 6px; font-size: 0.95rem; transition: all 0.2s; width: 100%; }
    
    .stButton>button:hover { background: #1f2937; }
    
    .result { border: 1px solid #e5e7eb; border-radius: 8px; padding: 2rem; margin-top: 2rem; }
    
    .result-title { font-size: 1.5rem; font-weight: 600; color: #111827; margin-bottom: 0.75rem; }
    
    .result-text { font-size: 0.95rem; color: #4b5563; line-height: 1.6; margin-bottom: 1.5rem; }
    
    .insight-section { margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb; }
    
    .insight-title { font-size: 1rem; font-weight: 600; color: #111827; margin-bottom: 1rem; }
    
    .insight-item { font-size: 0.9rem; color: #4b5563; margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative; }
    
    .insight-item:before { content: '•'; position: absolute; left: 0.5rem; color: #9ca3af; }
    
    .recommendation { background: #f9fafb; border-radius: 6px; padding: 1rem; margin-top: 1rem; }
    
    .recommendation-title { font-size: 0.9rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem; }
    
    .recommendation-text { font-size: 0.85rem; color: #6b7280; line-height: 1.5; }
    
    .risk-low { border-left: 3px solid #10b981; }
    
    .risk-moderate { border-left: 3px solid #f59e0b; }
    
    .risk-high { border-left: 3px solid #ef4444; }
    
    .footer { text-align: center; color: #9ca3af; font-size: 0.8rem; margin-top: 4rem; }
    
    hr { border: none; height: 1px; background: #e5e7eb; margin: 2.5rem 0; }
</style>œ
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1 class="main-title" style="color: #000000 !important;">StudentHealth360</h1><p class="subtitle">AI-Powered Student Wellness Risk Assessment</p></div>', unsafe_allow_html=True)

@st.cache_resource
def load_assets():
    try:
        return joblib.load('models/model.pkl'), joblib.load('models/scaler.pkl')
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None, None

model, scaler = load_assets()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<p class="section-title"><i class="fas fa-heartbeat"></i> Physiological</p>', unsafe_allow_html=True)
    age = st.number_input("Age", 17, 30, 20)
    heart_rate = st.number_input("Heart Rate (BPM)", 40.0, 150.0, 72.0)
    bp_systolic = st.number_input("Systolic BP", 80.0, 180.0, 120.0)
    bp_diastolic = st.number_input("Diastolic BP", 50.0, 120.0, 80.0)
    stress_bio = st.slider("Biosensor Stress", 1.0, 10.0, 5.0, help="Stress level measured by wearable biosensors (1=Low, 10=Extreme)")

with col2:
    st.markdown('<p class="section-title"><i class="fas fa-book"></i> Academic</p>', unsafe_allow_html=True)
    study_hours = st.number_input("Study Hours/Week", 0.0, 100.0, 30.0)
    project_hours = st.number_input("Project Hours/Week", 0.0, 100.0, 15.0)
    stress_self = st.slider("Self-Reported Stress", 1.0, 10.0, 5.0, help="Student's self-assessed stress level (1=Low, 10=Extreme)")
    activity = st.selectbox("Physical Activity", ["Low", "Moderate", "High"])

with col3:
    st.markdown('<p class="section-title"><i class="fas fa-brain"></i> Psychological</p>', unsafe_allow_html=True)
    sleep = st.selectbox("Sleep Quality", ["Poor", "Moderate", "Good"])
    mood = st.selectbox("Mood", ["Happy", "Neutral", "Stressed"])
    gender = st.selectbox("Gender", ["M", "F"])

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("Analyze Risk Profile", use_container_width=True):
    if model and scaler:
        activity_map = {'Low': 0, 'Moderate': 1, 'High': 2}
        sleep_map = {'Poor': 0, 'Moderate': 1, 'Good': 2}
        
        input_data = pd.DataFrame({
            'Age': [age], 'Heart_Rate': [heart_rate], 'Blood_Pressure_Systolic': [bp_systolic],
            'Blood_Pressure_Diastolic': [bp_diastolic], 'Stress_Level_Biosensor': [stress_bio],
            'Stress_Level_Self_Report': [stress_self], 'Physical_Activity': [activity_map[activity]],
            'Sleep_Quality': [sleep_map[sleep]], 'Study_Hours': [study_hours], 'Project_Hours': [project_hours],
            'Gender_F': [1 if gender == 'F' else 0], 'Gender_M': [1 if gender == 'M' else 0],
            'Mood_Happy': [1 if mood == 'Happy' else 0], 'Mood_Neutral': [1 if mood == 'Neutral' else 0],
            'Mood_Stressed': [1 if mood == 'Stressed' else 0]
        })
        
        num_cols = ['Heart_Rate', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic',
                    'Stress_Level_Biosensor', 'Stress_Level_Self_Report', 'Study_Hours', 'Project_Hours']
        input_data[num_cols] = scaler.transform(input_data[num_cols])
        
        prediction = model.predict(input_data)[0]
        
        # Generate insights
        total_hours = study_hours + project_hours
        stress_avg = (stress_bio + stress_self) / 2
        
        if prediction == 0:
            insights = f"""
            <div class="insight-section">
                <div class="insight-title">Key Observations</div>
                <div class="insight-item">Cardiovascular metrics within healthy range (HR: {heart_rate:.0f} BPM, BP: {bp_systolic:.0f}/{bp_diastolic:.0f})</div>
                <div class="insight-item">Balanced academic workload ({total_hours:.0f} hours/week) with {activity} physical activity</div>
                <div class="insight-item">Sleep quality rated as {sleep.lower()} with {mood.lower()} mood state</div>
                <div class="insight-item">Stress levels manageable (Avg: {stress_avg:.1f}/10)</div>
            </div>
            <div class="recommendation">
                <div class="recommendation-title"><i class="fas fa-lightbulb"></i> Recommendations</div>
                <div class="recommendation-text">Maintain current wellness practices. Consider periodic check-ins to sustain healthy patterns. Continue {activity.lower()} physical activity and prioritize {sleep.lower()} sleep quality.</div>
            </div>
            """
            st.markdown(f'<div class="result risk-low"><div class="result-title"><i class="fas fa-check-circle"></i> Low Risk</div><p class="result-text">Student metrics indicate healthy physiological and behavioral patterns across all measured dimensions.</p>{insights}</div>', unsafe_allow_html=True)
            st.balloons()
            
        elif prediction == 1:
            risk_factors = []
            if stress_avg > 6: risk_factors.append(f"Elevated stress levels (Avg: {stress_avg:.1f}/10)")
            if total_hours > 50: risk_factors.append(f"High academic workload ({total_hours:.0f} hours/week)")
            if sleep == "Poor": risk_factors.append("Poor sleep quality impacting recovery")
            if activity == "Low": risk_factors.append("Insufficient physical activity")
            if mood == "Stressed": risk_factors.append("Self-reported stressed mood state")
            if heart_rate > 85: risk_factors.append(f"Elevated resting heart rate ({heart_rate:.0f} BPM)")
            
            if not risk_factors:
                risk_factors = [f"Moderate stress indicators (Avg: {stress_avg:.1f}/10)", f"Academic load at {total_hours:.0f} hours/week"]
            
            insights = f"""
            <div class="insight-section">
                <div class="insight-title">Risk Factors Identified</div>
                {''.join([f'<div class="insight-item">{factor}</div>' for factor in risk_factors])}
            </div>
            <div class="recommendation">
                <div class="recommendation-title"><i class="fas fa-clipboard-list"></i> Action Plan</div>
                <div class="recommendation-text"><strong>Immediate:</strong> Schedule counseling session, review workload distribution<br>
                <strong>Short-term:</strong> Implement stress management techniques (meditation, breathing exercises)<br>
                <strong>Long-term:</strong> Establish sustainable study-life balance, increase physical activity to moderate/high levels</div>
            </div>
            """
            st.markdown(f'<div class="result risk-moderate"><div class="result-title"><i class="fas fa-exclamation-triangle"></i> Moderate Risk</div><p class="result-text">Early burnout indicators detected. Intervention at this stage can prevent escalation to critical levels.</p>{insights}</div>', unsafe_allow_html=True)
            
        else:
            critical_factors = []
            if stress_avg > 7: critical_factors.append(f"Critical stress levels (Avg: {stress_avg:.1f}/10)")
            if total_hours > 60: critical_factors.append(f"Excessive academic workload ({total_hours:.0f} hours/week)")
            if sleep == "Poor": critical_factors.append("Severe sleep deprivation affecting cognitive function")
            if activity == "Low": critical_factors.append("Sedentary lifestyle exacerbating stress response")
            if mood == "Stressed": critical_factors.append("Persistent stressed mood indicating mental health concern")
            if heart_rate > 90 or bp_systolic > 140: critical_factors.append("Cardiovascular stress markers elevated")
            
            if not critical_factors:
                critical_factors = [f"High stress levels (Avg: {stress_avg:.1f}/10)", f"Intensive workload ({total_hours:.0f} hours/week)", "Multiple risk factors converging"]
            
            insights = f"""
            <div class="insight-section">
                <div class="insight-title">Critical Concerns</div>
                {''.join([f'<div class="insight-item">{factor}</div>' for factor in critical_factors])}
            </div>
            <div class="recommendation">
                <div class="recommendation-title"><i class="fas fa-ambulance"></i> Urgent Intervention Required</div>
                <div class="recommendation-text"><strong>Immediate (24-48h):</strong> Contact campus wellness center, schedule emergency counseling, notify academic advisor<br>
                <strong>Medical:</strong> Consider physician consultation for cardiovascular and sleep assessment<br>
                <strong>Academic:</strong> Request course load reduction, deadline extensions, or temporary leave if necessary<br>
                <strong>Support:</strong> Activate peer support network, family notification recommended</div>
            </div>
            """
            st.markdown(f'<div class="result risk-high"><div class="result-title"><i class="fas fa-exclamation-circle"></i> High Risk</div><p class="result-text">Critical burnout detected with multiple physiological and psychological stress indicators. Immediate comprehensive intervention required.</p>{insights}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer"><i class="fas fa-shield-alt"></i> Educational tool only. Not a substitute for professional medical advice.</div>', unsafe_allow_html=True)
