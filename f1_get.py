from collections import namedtuple
import editor
import json
import os
import requests

race = namedtuple('race', 'season round time raceName date url Circuit')
url = 'http://ergast.com/api/f1/current.json'
filename = os.path.join(os.path.dirname(__file__), url.split('/')[-1])

r = requests.get(url)
r.raise_for_status()
data = r.json()
with open(filename, 'w') as out_file:    # avoid repeated API calls...
    json.dump(data, out_file, indent=2)  # by saving the data locally

races = [race(**r) for r in data['MRData']['RaceTable']['Races']]
print(races[6])
editor.open_file(filename)  # show the user the cached json data
