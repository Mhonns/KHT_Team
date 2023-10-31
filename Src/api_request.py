import requests
import json
import time

# Configuration
client_id = "1000.cdcfefa2eb93b29df7b6b856168beff9.fffa9eb94b050fc08acffb47925ca41c"
client_secret = "8c24c2333e50fd489fd869f725ef78d42feb25d739"
authen_code = input("Enter the authorization code from the redirect URL: ")

def get_access_token(code):
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    token_data = json.loads(response.text)
    if "error" in token_data:
        print(f"Error: {token_data['error']}")
        return None, None
    else:
        return token_data['access_token'], token_data['refresh_token']

def get_data(access_token):
    url = "https://www.zohoapis.com/crm/v5/Leads"
    params = {'fields': 'Last_Name,Company'}
    headers = {'Authorization': 'Zoho-oauthtoken {}'.format(access_token)}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        data = json.dumps(data, indent=2)
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

def get_new_access_token(refresh_token):
    refresh_url = "https://accounts.zoho.com/oauth/v2/token"
    param = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }
    response = requests.post(refresh_url, params=param)
    if response.status_code == 200:
        access_token = json.loads(response.text)["access_token"]
        data = response.json()
        data = json.dumps(data, indent=2)
        return access_token
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


access_token, refresh_token = get_access_token(authen_code)
count = 0

while True:
    if access_token != None:
        print("getting data...")
        data = get_data(access_token)
        print(data)
    # if count >= 10:
    #     if refresh_token != None:
    #         print("getting a new access token...")
    #         access_token = get_new_access_token(refresh_token)
    count += 1
    print("count {}".format(count))
    time.sleep(3)