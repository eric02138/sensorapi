import requests
import time
import random
from datetime import datetime

API_URL = 'http://localhost:5000/measurements'
response = requests.get(API_URL,  timeout=5)
print(response.status_code)
print(response.content)