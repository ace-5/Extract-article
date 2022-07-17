import requests
import json
from os.path import exists

base = 'https://bg.annapurnapost.com'
searchList = ['कोरोना भाइरस', 'कांग्रेस', 'एमाले', 'माओवादी केन्द्र'] # replace with search term of your choice

writeThis = {}
relativePath = None

for term in searchList:
    writeThis[term] = {}
    for i in range(3): # change 3 to 'n' to obtains articles of first n page(s)
        if exists('$term.json'):
            with open ('$term.json', 'r+') as f:
                file_data = json.loads(f.read())
                # if current search term is already in file retrive next page link value
                if term in file_data.keys():
                    relativePath = file_data[term]['next']
                    response = requests.get(base+relativePath)
                    response_data = json.loads(response.text)
                    file_data[term]['articles'].extend(response_data['data']['items'])
                    file_data[term]['next'] = response_data['data']['links']['next']
                    f.seek(0)
                    f.write(json.dumps(file_data, ensure_ascii=False, indent=2))
                # if current search term is not in file, set it's first page link as relative path 
                else:
                    relativePath = f'/api/search?title={term}'
                    response = requests.get(base+relativePath)
                    response_data = json.loads(response.text)
                    file_data[term] = {}
                    file_data[term]['articles'] = response_data['data']['items']
                    file_data[term]['next'] = response_data['data']['links']['next']
                    f.seek(0)
                    f.write(json.dumps(file_data, ensure_ascii=False, indent=2))
                
        # if file does not exist create a file and write it with response of initial request
        # runs only once if the file is not deleted locally 
        else:
            relativePath = f'/api/search?title={term}' 
            with open('$term.json', 'w') as f:
                response = requests.get(base+relativePath)
                response_data = json.loads(response.text)
                writeThis[term]['articles'] = response_data['data']['items']
                writeThis[term]['next'] = response_data['data']['links']['next']
                f.write(json.dumps(writeThis, ensure_ascii=False, indent=2))