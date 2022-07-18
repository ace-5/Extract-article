import requests
import json
from os.path import exists
base = 'https://bg.annapurnapost.com'
searchList = ['कोरोना भाइरस', 'कांग्रेस', 'एमाले', 'माओवादी केन्द्र']


writeThis = {}
for term in searchList:
  for i in range(3):
    if exists(f'./{term}.json'):
      with open(f'{term}.json', 'r+') as f:
        writeThis = json.loads(f.read())
        relativePath = writeThis['next']
        response = requests.get(base+relativePath)
        data = json.loads(response.text)
        writeThis['articles'].extend(data['data']['items'])
        writeThis['next'] = data['data']['links']['next']
        f.seek(0)
        f.write(json.dumps(writeThis, ensure_ascii = False, indent=2))


  # if the file doesn't exist for current term
  # only runs once per term
    else:
      relativePath = f'/api/search?title={term}'
      response = requests.get(base+relativePath)
      data = json.loads(response.text)
      with open(f'{term}.json', 'w') as f:
        writeThis['articles'] = data['data']['items']
        writeThis['next'] = data['data']['links']['next']
        f.write(json.dumps(writeThis, ensure_ascii = False, indent=2))