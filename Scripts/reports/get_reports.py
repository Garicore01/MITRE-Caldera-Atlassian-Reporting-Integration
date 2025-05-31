import requests

# Extract the api_key from the .env file 
with open("../.env", "r") as f:
    lines = f.readlines()
    caldera_server = lines[0].split("=")[1].strip()
    api_key = lines[1].split("=")[1].strip()
        

api_url = f"http://{caldera_server}/api/v2"
headers = {
    "KEY": api_key
}

response = requests.post(f"{api_url}/operations/560363bd-f05f-4227-ab15-bda25f5ef31f/report", 
                         headers=headers)

if response.status_code == 200:
    with open("report.json", "wb") as f:
        f.write(response.content)
else:
    print(f"Failed to get operations: {response.text}")
