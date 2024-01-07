import requests
import json

url = "http://localhost:5000/reserve"  # replace with your actual server URL
data = {
    "id": '1',  # replace with your actual clinic id
    "reserved": 5  # replace with the actual number of slots to reserve
}

response = requests.post(url, data=json.dumps(data))

