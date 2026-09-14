#dirtspore.py
import json
import urllib.request

dirtspore_url = 'https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/quantumnoiseradio/dirt.json'

try:
    with urllib.request.urlopen(dirtspore_url) as response:
        dirtspore = json.loads(response.read().decode('utf-8'))
except Exception as e:
    dirtspore = {"files": []}

files_root = dirtspore_url.split("dirt.json")[0]

for file in dirtspore.get('files', []):
    remote_url = files_root + file
    print(remote_url)
    try:
        urllib.request.urlretrieve(remote_url, file)
    except Exception as e:
        pass

