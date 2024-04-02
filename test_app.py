import requests
import os
URL = 'http://127.0.0.1:5000/api/id-card-detection/process-image'
IMG_PATH = 'uploads/IMG-20220810-WA0175_jpg.rf.f448ce74910236e77cd9cbf9bc6dba23.jpg'


try:
    img_path = os.path.join(os.getcwd(), IMG_PATH)
    files = {'file': open(img_path, 'rb')}
    response = requests.post(URL, files=files)
    print(response.json())
except Exception as e:
    print(e)
