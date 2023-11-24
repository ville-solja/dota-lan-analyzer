import requests
import json

#Token for access
with open('token.txt', 'r') as f:
    token = f.read()

#GraphQL endpoint URL
url = 'https://api.stratz.com/graphql'

#Headers for the request
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

def process_matches(match_list, players):
    responses = {}
    for player in players:
        responses[player] = []
    with open(match_list) as matches:
        for match in matches:
            match_name = match.strip()
            response = fetch_match_data(match)
            for player in (response["data"]["match"]["players"]):
                if player["steamAccountId"] in players.values():
                    result_temp = [match_name,player["imp"],player["goldPerMinute"],player["experiencePerMinute"]]
                    player_name =  {i for i in players if players[i]==player["steamAccountId"]}
                    player_name = player_name.pop()
                    result = responses[player_name]
                    result.append(result_temp)
                    responses[player_name] = result
    return responses
 
def find_player(player_list):
    players_list = {}
    with open(player_list) as players:
        for player in players:
            response = fetch_player_data(player)
            id = response["data"]["player"]["steamAccount"]["id"]
            name = response["data"]["player"]["steamAccount"]["name"]
            players_list[name] = id
    return players_list

#main script
def main():
    players = find_player('playerlist.txt')
    print(process_matches('matchlist.txt', players))

if __name__ == "__main__":
    main()

