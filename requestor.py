import json
import requests
import time
import random
from datetime import datetime

# Retrieves a list of distinct sensor ids
# MEASUREMENTS_API_URL = 'http://localhost:5000/measurements'
# response = requests.get(MEASUREMENTS_API_URL,  timeout=5)
# print(response.status_code)
# print(json.loads(response.content))

# Retrieves aggregated data for the last hour in 5 minute chunks for sensor_001
SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_001'
response = requests.get(SENSOR_API_URL,  timeout=5)
print(response.status_code)
print(json.loads(response.content))

# Retrieves aggregated data for the last hour in 5 minute chunks for sensor_002
# SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_002'
# response = requests.get(SENSOR_API_URL,  timeout=5)
# print(response.status_code)
# print(json.loads(response.content))

# Retrieves aggregated data for an hour for sensor_003
# SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_003?end_dt=2025-11-21T17:55:41'
# response = requests.get(SENSOR_API_URL,  timeout=5)
# print(response.status_code)
# print(json.loads(response.content))

# Retrieves aggregated data for an hour for sensor_002
# SENSOR_API_URL = 'http://localhost:5000/measurements/sensor_002?end_dt=2025-11-21T17:55:41'
# response = requests.get(SENSOR_API_URL,  timeout=5)
# print(response.status_code)
# print(json.loads(response.content))