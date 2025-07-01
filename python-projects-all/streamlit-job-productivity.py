import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.title("📊 Office Productivity Issue Predictor")

# Sample data generation (in a real app, you'd upload CSV)
@st.cache_data
def load_sample_data():
    data = {
        'age': [25, 30, 45, 33, 28, 50, 22, 35],
        'role': ['Developer', 'Designer', 'Manager', 'Analyst', 'Developer', 'Manager', 'Intern', 'Designer'],
        'work_hours': [9, 8, 10, 7, 9, 8, 6, 8],
        'screen_time': [7, 6, 5, 8, 9, 4, 7, 6],
        'breaks': ['Regular', 'Rare', 'Regular', 'None', 'Rare', 'Regular', 'None', 'Regular'],
        'workstation': ['Ergonomic', 'Basic', 'Ergonomic', 'Basic', 'Basic', 'Ergonomic', 'Basic', 'Ergonomic'],
        'noise_level': ['Low', 'Medium', 'High', 'Medium', 'High', 'Low', 'Medium', 'Low'],
        'issue': ['Eye strain', 'Creativity block', 'Burnout', 'Neck pain', 'Focus issues', 'Stress', 'Fatigue', 'Back pain']
    }
    return pd.DataFrame(data)

df = load_sample_data()

if st.checkbox("Show sample dataset"):
    st.write("💼 Sample Office Productivity Dataset:")
    st.dataframe(df)

# Encoding
le_role = LabelEncoder()
le_breaks = LabelEncoder()
le_workstation = LabelEncoder()
le_noise = LabelEncoder()
le_issue = LabelEncoder()

df['role_enc'] = le_role.fit_transform(df['role'])
df['breaks_enc'] = le_breaks.fit_transform(df['breaks'])
df['workstation_enc'] = le_workstation.fit_transform(df['workstation'])
df['noise_enc'] = le_noise.fit_transform(df['noise_level'])
df['issue_enc'] = le_issue.fit_transform(df['issue'])

# Model training
X = df[['age', 'role_enc', 'work_hours', 'screen_time', 'breaks_enc', 'workstation_enc', 'noise_enc']]
y = df['issue_enc']

model = RandomForestClassifier()
model.fit(X, y)

# User input
st.subheader("🖥️ Enter Your Work Details")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=18, max_value=65, value=30)
    role = st.selectbox("Job Role", le_role.classes_)
    work_hours = st.slider("Daily Work Hours", 4, 12, 8)
    
with col2:
    screen_time = st.slider("Screen Time (hours)", 4, 12, 8)
    breaks = st.selectbox("Break Frequency", le_breaks.classes_)
    workstation = st.selectbox("Workstation Type", le_workstation.classes_)
    noise_level = st.selectbox("Noise Level", le_noise.classes_)

# Prediction
if st.button("Predict Productivity Issue"):
    input_data = [[
        age,
        le_role.transform([role])[0],
        work_hours,
        screen_time,
        le_breaks.transform([breaks])[0],
        le_workstation.transform([workstation])[0],
        le_noise.transform([noise_level])[0]
    ]]
    
    prediction = model.predict(input_data)
    issue = le_issue.inverse_transform(prediction)[0]
    
    st.error(f"⚠️ Predicted Productivity Challenge: **{issue}**")
    
    # Suggestions based on prediction
    st.subheader("💡 Improvement Suggestions")
    if 'strain' in issue.lower():
        st.write("- Follow the 20-20-20 rule (every 20 mins, look 20 feet away for 20 seconds)")
    elif 'pain' in issue.lower():
        st.write("- Adjust chair height so feet rest flat, take micro-stretch breaks")
    elif 'focus' in issue.lower():
        st.write("- Try Pomodoro technique (25 min focused work + 5 min break)")