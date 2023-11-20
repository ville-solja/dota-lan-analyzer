import requests
import json

# Token for access
with open('token.txt', 'r') as f:
    token = f.read()

# GraphQL endpoint URL
url = 'https://api.stratz.com/graphql'
# Headers for the request
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(token)
}

def fetch_match_data(matchid):
    graphql_match_query = '''
        query {  
            match(id: %s) {
                players {
                    steamAccountId
                    heroId
                    role
                    kills
                    deaths
                    assists
                    goldPerMinute
                    experiencePerMinute
                    imp
                }
            }
        }
        ''' % matchid

    request_data = {
        'query': graphql_match_query,
    }
    response = requests.post(url, headers=headers, json=request_data).json()
    return response

def fetch_player_data(steamAccountId):
    graphql_player_query = '''
        query {  
            player(steamAccountId: %s) {
                steamAccount {
                    name
                    id
                }
            }
        }
        ''' % steamAccountId

    request_data = {
        'query': graphql_player_query,
    }
    response = requests.post(url, headers=headers, json=request_data).json()
    return response

def process_response(response):
    if response.status_code == 200:
        data = json.loads(response.text)
        #print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}\n{response.text}")
    return json.dumps(data, indent=2)

#main script
with open('matchlist.txt') as matches:
    for match in matches:
        response = fetch_match_data(match)
        print(response)
        break
