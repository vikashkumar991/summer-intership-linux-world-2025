import streamlit as st
import pandas as ps
from sklearn.linear_model import LinearRegression

st.title("predict salary")

file = st.file_uploader("upload your file", type=["csv"])

if file is not None:
    data = ps.read_csv(file)
    age = data
    st.write(data)
    brain = LinearRegression()
    brain.fit(data[["exp"]],data[["salary"]])
    age = st.number_input("Enter age: ")
    result = brain.predict([[age]])
    salary = float(result[0])  # Convert from array to single number
    st.success(f"Predicted salary is ₹{salary:,.2f}")
