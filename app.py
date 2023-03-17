import requests
import json

RES = json.loads(requests.get('http://localhost:3000/getHistoryUnique?stock=MXRF11&range=max').text)

with open('resposta.json', 'w') as f:
    json.dump(RES, f)