#pip install requests

import requests
import base64
import glob
import json
from datetime import datetime
import urllib3
urllib3.disable_warnings()

# Proxy để máy nội bộ có thể kết nối đến trang pentest
exec(base64.b64decode('cHJveHkgPSB7J2h0dHBzJzpiYXNlNjQuYjY0ZGVjb2RlKCdhSFIwY0Rvdkx6RTVNaTR4TmpndU5TNDRPak14TWpnPScpLmRlY29kZSgpfQ=='))

# Nếu script không chạy trong máy nội bộ, hãy set giá trị là None, hoặc Burp Proxy
# proxy = None

# 1. refresh_token lấy tại Local Storage trang pentest sau khi đăng nhập
refresh_token = ''

# 2. Phần đầu của các file muốn upload
# vd: các file là Google.zip.001, Google.zip.002 => pattern='Google'
pattern = '' 

# base64 domain, né search :))
exec(base64.b64decode('ZG9tYWluID0gYmFzZTY0LmI2NGRlY29kZSgnY0dWdWRHVnpkQzUyYVdWMGRHVnNZM2xpWlhJdVkyOXQnKS5kZWNvZGUoKQ=='))

def encode_file_to_base64(input_file_path):
    with open(input_file_path, "rb") as input_file:
        encoded_bytes = base64.b64encode(input_file.read())
        return encoded_bytes.decode("utf-8")

token = ''
exp = 0

def get_exp(token):
    payload = token.split('.')[1]
    payload = payload + '=' * (-len(payload) % 4)
    return int(json.loads(base64.b64decode(payload).decode())['exp'])

def check_token():
    global token
    global exp
    if exp > datetime.timestamp(datetime.now()) + 10:
        return
    try:
        url = f'https://{domain}/api/v1/token/refresh'
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'token':refresh_token})
        response = requests.post(url, headers=headers, data=data, proxies=proxy, timeout=3, verify=False)
        token = response.json()['token']
        exp = get_exp(token)
        print("check_token(): OK")
    except:
        print("refresh_token() false - Check again!")
        check_token()


def uploadfile(filename):
    check_token()
    url = f'https://{domain}/attachments'
    headers = {
        'Content-Type': 'application/json',
        'Token': token
    }
    try:
        data = json.dumps({"content":encode_file_to_base64(filename),"name":f'{filename}.docx'})
        response = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
        return response.json()
    except:
        print(f"Upload {filename} false - Upload again!")
        return uploadfile(filename)

output = ''
matching_files = glob.glob(f'{pattern}*')

for file in matching_files:
    output += f'curl "https://{domain}/{uploadfile(file)["path"]}" -o "{file}"\n'
    print(f'Done {file}')

open(f'output - {pattern}.bat', 'w').write(output)
print('Done All!')