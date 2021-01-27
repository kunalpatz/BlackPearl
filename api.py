import requests

import json

from database.models import App


def ip_address(ip):
    data = App.objects(name="virustotal")[0]
    api = json.loads(data.to_json())['site'] + "ip_addresses/" + ip
    headers = {
        'x-apikey': json.loads(data.to_json())['key']
    }
    payload = {}
    response = requests.request("GET", api, headers=headers, data=payload)
    return response.json()


# response = ip_address('146.59.196.21')

# with open('ip_data.json', 'w') as outfile:
#    json.dump(response, outfile)

def domain(domain):
    api = "https://www.virustotal.com/api/v3/domains/" + domain
    headers = {
        'Authorization': 'Basic Og==',
        'x-apikey': '<your apikey>'
    }
    payload = {}
    response_url = requests.request("GET", api, headers=headers, data=payload)
    return response_url.json()
