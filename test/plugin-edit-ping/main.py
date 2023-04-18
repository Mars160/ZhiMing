from requests import get

URL = "http://127.0.0.1:5000/v1/ping"

req = get(URL)

print(req.text)