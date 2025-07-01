import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

st.title("🧳 Travel Package Recommender")

# Upload CSV
file = st.file_uploader("Upload travel dataset CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.write("📊 Dataset Preview", df)

    # Encode categorical columns
    le_dest = LabelEncoder()
    le_package = LabelEncoder()

    df["preferred_destination_encoded"] = le_dest.fit_transform(df["preferred_destination"])
    df["package_type_encoded"] = le_package.fit_transform(df["package_type"])

    # Prepare training data
    X = df[["age", "income", "preferred_destination_encoded"]]
    y = df["package_type_encoded"]

    # Train model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # User Input
    st.subheader("📥 Enter Traveller Details:")
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    income = st.number_input("Monthly Income (₹)", value=30000)
    destination = st.selectbox("Preferred Destination", le_dest.classes_)

    # Prediction
    dest_encoded = le_dest.transform([destination])[0]
    prediction = model.predict([[age, income, dest_encoded]])
    predicted_label = le_package.inverse_transform(prediction)[0]

    st.success(f"🎯 Recommended Travel Package: **{predicted_label}** {prediction}")
