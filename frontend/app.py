import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Lead Conversion Prediction Application")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for lead features
age = st.number_input("Age", min_value=18, max_value=100, value=30)
current_occupation = st.selectbox("Current Occupation", ['Professional', 'Unemployed', 'Student'])
first_interaction = st.selectbox("First Interaction", ['Website', 'Mobile App'])
profile_completed = st.selectbox("Profile Completed", ['Low', 'Medium', 'High'])
website_visits = st.number_input("Website Visits", min_value=0, value=5)
time_spent_on_website = st.number_input("Time Spent on Website (seconds)", min_value=0, value=500)
page_views_per_visit = st.number_input("Page Views Per Visit", min_value=0.0, value=3.0)
last_activity = st.selectbox("Last Activity", ['Email Activity', 'Website Activity', 'Phone Activity'])
print_media_type1 = st.selectbox("Saw Ad in Print Media Type 1?", ['No', 'Yes'])
print_media_type2 = st.selectbox("Saw Ad in Print Media Type 2?", ['No', 'Yes'])
digital_media = st.selectbox("Saw Ad on Digital Media?", ['No', 'Yes'])
educational_channels = st.selectbox("Heard via Educational Channels?", ['No', 'Yes'])
referral = st.selectbox("Came via Referral?", ['No', 'Yes'])

# Convert user input into a dictionary
input_data_dict = {
    'age': age,
    'current_occupation': current_occupation,
    'first_interaction': first_interaction,
    'profile_completed': profile_completed,
    'website_visits': website_visits,
    'time_spent_on_website': time_spent_on_website,
    'page_views_per_visit': page_views_per_visit,
    'last_activity': last_activity,
    'print_media_type1': print_media_type1,
    'print_media_type2': print_media_type2,
    'digital_media': digital_media,
    'educational_channels': educational_channels,
    'referral': referral
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict Lead Conversion", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data_dict)  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Conversion Status']
        if prediction == 1:
            st.success("Predicted Conversion Status: CONVERTED")
        else:
            st.warning("Predicted Conversion Status: NOT CONVERTED")
    else:
        st.error(f"Unable to connect to the prediction API. Error: {response.text}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch from CSV", type="primary"):
        files = {'file': uploaded_file.getvalue()} # Get the byte content of the uploaded file
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            # Convert predictions dictionary to DataFrame for better display
            predictions_df = pd.DataFrame(list(predictions.items()), columns=['Lead ID', 'Predicted Status'])
            predictions_df['Predicted Status'] = predictions_df['Predicted Status'].map({1: 'CONVERTED', 0: 'NOT CONVERTED'})
            st.write(predictions_df)  # Display the predictions
        else:
            st.error(f"Unable to connect to the prediction API for batch prediction. Error: {response.text}")
