import urllib.request, json, sys

data_str = sys.stdin.read()
posts = json.loads(data_str)
name = posts['name']
body = posts['posts']

req = urllib.request.Request(f'http://127.0.0.1:8765/raw/{name}', data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    print(resp.read().decode('utf-8'))
