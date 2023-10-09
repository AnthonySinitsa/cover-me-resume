import os
import json

# Get the service account info from the environment variable
service_account_info = os.environ.get('GS_CREDENTIALS')

if service_account_info:
    # Parse the JSON string and write it to a file
    with open('service-account.json', 'w') as file:
        json_info = json.loads(service_account_info)
        json.dump(json_info, file)
