import json
import requests
import time
import random
from datetime import datetime

MEASUREMENTS_API_URL = 'http://localhost:5000/measurements'
response = requests.get(MEASUREMENTS_API_URL,  timeout=5)
print(response.status_code)
print(json.loads(response.content))

SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_001'
response = requests.get(SENSOR_API_URL,  timeout=5)
print(response.status_code)
print(json.loads(response.content))

SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_002'
response = requests.get(SENSOR_API_URL,  timeout=5)
print(response.status_code)
print(json.loads(response.content))

SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_003?end_dt=2025-11-21T17:55:41'
response = requests.get(SENSOR_API_URL,  timeout=5)
print(response.status_code)
print(json.loads(response.content))

SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_002?end_dt=2025-11-21T17:55:41Z'
response = requests.get(SENSOR_API_URL,  timeout=5)
print(response.status_code)
print(json.loads(response.content))