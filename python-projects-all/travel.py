import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

st.title("🧳 Journey Issue Predictor")

# Upload CSV
file = st.file_uploader("Upload Journey Dataset CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.write("📄 Dataset Preview", df)

    # Encode categorical columns
    le_gender = LabelEncoder()
    le_dest = LabelEncoder()
    le_mode = LabelEncoder()
    le_season = LabelEncoder()
    le_health = LabelEncoder()
    le_issue = LabelEncoder()

    df["gender_enc"] = le_gender.fit_transform(df["gender"])
    df["dest_enc"] = le_dest.fit_transform(df["destination"])
    df["mode_enc"] = le_mode.fit_transform(df["travel_mode"])
    df["season_enc"] = le_season.fit_transform(df["season"])
    df["health_enc"] = le_health.fit_transform(df["health_issues"])
    df["issue_enc"] = le_issue.fit_transform(df["issue"])

    # Model training
    X = df[["age", "gender_enc", "dest_enc", "mode_enc", "season_enc", "health_enc"]]
    y = df["issue_enc"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    # User input
    st.subheader("🎫 Enter Journey Details:")
    age = st.number_input("Age", min_value=10, max_value=100, value=30)
    gender = st.selectbox("Gender", le_gender.classes_)
    destination = st.selectbox("Destination", le_dest.classes_)
    travel_mode = st.selectbox("Travel Mode", le_mode.classes_)
    season = st.selectbox("Season", le_season.classes_)
    health = st.selectbox("Pre-existing Health Issues", le_health.classes_)

    # Encode input
    user_data = [[
        age,
        le_gender.transform([gender])[0],
        le_dest.transform([destination])[0],
        le_mode.transform([travel_mode])[0],
        le_season.transform([season])[0],
        le_health.transform([health])[0]
    ]]

    prediction = model.predict(user_data)
    issue_result = le_issue.inverse_transform(prediction)[0]

    st.success(f"⚠️ Predicted Journey Issue: **{issue_result}**")

