import streamlit as st
import requests
import os 

BACKEND_URL = os.getenv("BACKEND_URL", "http://0.0.0.0:8000")

def check_health():
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to backend: {str(e)}"}

def predict(data):
    try:
        response = requests.post(f"{BACKEND_URL}/predict", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Prediction failed: {str(e)}"}

def predict_batch(file):
    try:
        # Send the uploaded file to the backend
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{BACKEND_URL}/predict_batch", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Batch prediction failed: {str(e)}"}

st.title("Backend Interaction")

with st.expander("Health Check", expanded=False):
    if st.button("Check Health"):
        health_status = check_health()
        if "error" in health_status:
            st.error(f"Error: {health_status['error']}")
        else:
            st.success("Backend is healthy!")
            st.write("Health Status:", health_status)

with st.expander("Predict", expanded=False):
    with st.form("predict_form"):
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        job = st.text_input("Job", "unemployed")
        marital = st.text_input("Marital", "single")
        education = st.text_input("Education", "primary")
        default = st.text_input("Default", "no")
        balance = st.number_input("Balance", min_value=-10000, max_value=100000, value=0)
        housing = st.text_input("Housing", "no")
        loan = st.text_input("Loan", "no")
        contact = st.text_input("Contact", "cellular")
        day = st.number_input("Day", min_value=1, max_value=31, value=1)
        month = st.text_input("Month", "jan")
        duration = st.number_input("Duration", min_value=0, max_value=5000, value=180)
        campaign = st.number_input("Campaign", min_value=1, max_value=50, value=1)
        pdays = st.number_input("Pdays", min_value=-1, max_value=1000, value=-1)
        previous = st.number_input("Previous", min_value=0, max_value=10, value=0)
        poutcome = st.text_input("Poutcome", "nonexistent")

        submitted = st.form_submit_button("Submit")
        if submitted:
            data = {
                "age": age,
                "job": job,
                "marital": marital,
                "education": education,
                "default": default,
                "balance": balance,
                "housing": housing,
                "loan": loan,
                "contact": contact,
                "day": day,
                "month": month,
                "duration": duration,
                "campaign": campaign,
                "pdays": pdays,
                "previous": previous,
                "poutcome": poutcome
            }
            prediction = predict(data)
            if "error" in prediction:
                st.error(f"Error: {prediction['error']}")
            else:
                st.success("Prediction completed!")
                st.write("Prediction:", prediction)

with st.expander("Predict Batch", expanded=False):
    batch_file = st.file_uploader("Choose a file")
    if st.button("Predict Batch"):
        if batch_file is not None:
            prediction_batch = predict_batch(batch_file)
            if "error" in prediction_batch:
                st.error(f"Error: {prediction_batch['error']}")
            else:
                st.success("Batch prediction completed!")
                st.write("Batch Prediction:", prediction_batch)
        else:
            st.warning("Please upload a file first")
