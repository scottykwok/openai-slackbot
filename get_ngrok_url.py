import requests
r = requests.get('http://localhost:4040/api/tunnels')
datajson = r.json()
msg = ""
for i in datajson['tunnels']:
    msg = msg + i['public_url'] + '\n'
print(msg)