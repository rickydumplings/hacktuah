import requests
from dotenv import load_dotenv
import os

load_dotenv()
# print(os.getcwd())

API_KEY = os.getenv("SINGLE_API")

# Set up the URL and API key
url = 'https://svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com/api/v2/exec'
headers = {
    f'Authorization': f'Bearer {API_KEY}',
    'accept': 'application/json',
}

# SQL query to retrieve data
query = {
    'sql': 'SELECT label, value FROM entities;'
}

# Send the POST request
response = requests.post(url, json=query, headers=headers)

# Check for a successful response
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print("Data retrieved successfully:", data)
else:
    print("Error retrieving data:", response.status_code, response.text)
