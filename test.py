import json

import requests

url="http://localhost:5000/flag"
token="LJ425uyaTegD6pKxIdm7WZPcYRkwXHtq"
flag={"flag":"BiuCtf{RjZGYk98-1Vm76fcG-X1lJZjPn-cgEYt3Vd}"}
def main():
    headers = {
        "Authorization": token,
    }
    resp = requests.post(url=url, headers=headers,data=json.dumps(flag))
    print(resp.text)
    return

if __name__ == '__main__':
    main()