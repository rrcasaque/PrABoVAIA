import requests
import json

RES = json.loads(requests.get('http://localhost:3000/getHistory').text)

with open('resposta.json', 'w') as f:
    json.dump(RES, f)