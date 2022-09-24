import requests
import json

raw_create_response = requests.post('http://0.0.0.0:8080/user/create', headers = {"accept": "application/json"})
create_response = json.loads(raw_create_response.content)

print(create_response)

raw_info_response = requests.post('http://0.0.0.0:8080/user/info', headers = {"Authorization": "Bearer " + create_response["access_token"]})
info_response = json.loads(raw_info_response.content)

print(info_response)

