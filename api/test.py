import requests

BASE_URL= "http://127.0.0.1:5000/"

response= requests.put(BASE_URL+"hello/")
#response= requests.get(BASE_URL+"hello/Priya/1")
#response= requests.get(BASE_URL+"hello")
#response= requests.post(BASE_URL+"hello")
print(response.json())
