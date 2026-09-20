# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
lead_prediction_api = Flask("Lead Prediction API")

# Load the trained machine learning model
model = joblib.load("deployment_files/lead_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@lead_prediction_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Lead Conversion Prediction API!"

# Define an endpoint for single lead prediction (POST request)
@lead_prediction_api.post('/v1/predict')
def predict_lead_conversion():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing lead details and returns
    the predicted conversion status (0 or 1) as a JSON response.
    """
    # Get the JSON data from the request body
    lead_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'age': lead_data['age'],
        'current_occupation': lead_data['current_occupation'],
        'first_interaction': lead_data['first_interaction'],
        'profile_completed': lead_data['profile_completed'],
        'website_visits': lead_data['website_visits'],
        'time_spent_on_website': lead_data['time_spent_on_website'],
        'page_views_per_visit': lead_data['page_views_per_visit'],
        'last_activity': lead_data['last_activity'],
        'print_media_type1': lead_data['print_media_type1'],
        'print_media_type2': lead_data['print_media_type2'],
        'digital_media': lead_data['digital_media'],
        'educational_channels': lead_data['educational_channels'],
        'referral': lead_data['referral']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_status = model.predict(input_data)[0]

    # Return the predicted status
    return jsonify({'Predicted Conversion Status': int(predicted_status)})


# Define an endpoint for batch prediction (POST request)
@lead_prediction_api.post('/v1/predictbatch')
def predict_lead_conversion_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing lead details for multiple leads
    and returns the predicted conversion statuses as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all leads in the DataFrame
    predicted_statuses = model.predict(input_data).tolist()

    # Create a dictionary of predictions with lead IDs as keys
    # Assuming 'ID' is the lead ID column in the uploaded CSV
    lead_ids = input_data['ID'].tolist() 
    output_dict = dict(zip(lead_ids, [int(status) for status in predicted_statuses]))

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    lead_prediction_api.run(debug=True)
