import time
import requests
import urllib.parse
import hashlib
import hmac
import base64

with open ("KEYS.txt","r") as f:
    lines = f.read().splitlines()
    api_key = lines[0]
    api_secret = lines[1]


api_url = "https://api.kraken.com"

# signiature to send with request for verification
def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def kraken_request(url_path, data, api_key, api_secret):
    headers = {"API-Key": api_key, "API-Sign": get_kraken_signature(url_path, data, api_secret)}
    resp = requests.post((api_url + url_path), headers=headers, data=data)
    return resp

#URL PATH TO GET BALANCE
resp = kraken_request("/0/private/Balance", {"nonce": str(int(1000 * time.time()))} , api_key, api_secret)

print (resp.json()["result"])