config = {
    'host': '127.0.0.1',
    'port': 3310,
    'user': 'root',
    'password': 'augurs',
    'database': 'flightwatchers'
}

import requests

# apiKey = input("API Key: ")
# apiUrl = "https://aeroapi.flightaware.com/aeroapi/"
#
# airport = 'KSFO'
# payload = {'max_pages': 2}
# auth_header = {'x-apikey':apiKey}
#
# response = requests.get(apiUrl + f"airports/{airport}/flights",
#     params=payload, headers=auth_header)
#
# if response.status_code == 200:
#     print(response.json())
# else:
#     print("Error executing request")