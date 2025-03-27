import json
import requests

# API endpoint
API_URL = "http://10.0.19.247:8000/api/car_attributes/"

# Load car features JSON
with open("car_features.json", "r") as file:
    car_features_data = json.load(file)

# Check if the data is a dictionary or list
if isinstance(car_features_data, dict):  # If single object, wrap in a list
    car_features_data = [car_features_data]

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send POST request
response = requests.post(API_URL, json=car_features_data, headers=headers)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
