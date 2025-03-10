# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import re

with open("../.env", "r") as f:
    lines = f.readlines()
    atlassian_url = re.search(r'atlassian_url\s*=\s*(.*)', lines[2]).group(1).strip()
    atlassian_token = re.search(r'atlassian_token\s*=\s*(.*)', lines[3]).group(1).strip()
    atlassian_email = re.search(r'atlassian_email\s*=\s*(.*)', lines[4]).group(1).strip()

url = atlassian_url + "/1032880265"

auth = HTTPBasicAuth(atlassian_email, atlassian_token)

headers = {
  "Accept": "application/json",
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))





