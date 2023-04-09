from requests import post, get
from time import sleep

path = 'http://127.0.0.1:5000/v1/plugin/ocr'

req = post(path, files={'file': open('test.jpg', 'rb')})
try:
    uuid = req.json()['data']
    print(uuid)

    while True:
        req = get(path + '/' + uuid)
        data = req.json()['data']
        if data != None:
            print(data)
            break
        else:
            print(req.json()['msg'])
        sleep(1)
except:
    print(req.text)
