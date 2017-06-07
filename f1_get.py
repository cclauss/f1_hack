from collections import namedtuple
import json
import os
import requests

try:
    import editor  # if running on http://omz-software.com/pythonista/
except InportError:
    editor = None

race = namedtuple('race', 'season round time raceName date url Circuit')
url = 'https://ergast.com/api/f1/current.json'
filename = os.path.join(os.path.dirname(__file__), url.split('/')[-1])

r = requests.get(url)
r.raise_for_status()
data = r.json()
with open(filename, 'w') as out_file:    # avoid repeated API calls...
    json.dump(data, out_file, indent=2)  # by saving the data locally

races = [race(**r) for r in data['MRData']['RaceTable']['Races']]
print(races[6])
if editor:  # if running on http://omz-software.com/pythonista/
    editor.open_file(filename)  # show the user the cached json data

'''
    https://stackoverflow.com/questions/8335096/iterate-over-nested-dictionary
'''
# the code below from stackflow is what i think we will need to generically process the 
# returned json/dict. well at least the start anyway... IanJ
def recurse(d, keys=()):
    if isinstance(d, dict):
         for key, value in d.items():
            for rv in recurse(value, keys + (key, )):
                yield rv
    else:
        yield (keys, d)

#for compound_key, val in recurse(data):
    #print('{}: {}'.format(compound_key, val))
    
for compound_key, val in recurse(data):
    print('{}'.format(compound_key))
