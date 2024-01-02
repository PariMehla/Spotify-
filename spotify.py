import requests

# Constants
CLIENT_ID = 'a1211eeec3424ffca8fc6f8dbee1b6ca'
CLIENT_SECRET = 'a668e7d0f7fd42d9940f6d33b12c820d'
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

# Authentication
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

try:
    auth_response.raise_for_status()
    access_token = auth_response.json()['access_token']
except requests.exceptions.HTTPError as err:
    print(f"Authentication failed: {err}")
    exit()

# Functions
def input_decider(choice):
    return {1: 'track', 2: 'album', 3: 'artist'}.get(choice)

# Main loop
while True:
    # User input
    choice = int(input("\nWhat would you like to search up?\n\t1 - Track\n\t2 - Album\n\t3 - Artist\n\t4 - All\n"))

    while choice not in {1, 2, 3, 4}:
        choice = int(input("Please type a number between 1 and 4: "))

    # Search input
    search = input("\nWhat would you like to search up?\n")

    # API query
    if choice == 4:
        query = {'q': search, 'type': 'track,album,artist', 'limit': 10}
    else:
        query = {'q': search, 'type': input_decider(choice), 'limit': 10}

    response = requests.get(BASE_URL + 'search', params=query, headers={'Authorization': 'Bearer ' + access_token})
    response.raise_for_status()
    result = response.json()

    # Print results
    if choice == 4:
        for category in ['tracks', 'albums', 'artists']:
            print(f"\n{category.capitalize()}\n{'-'*76}\n")
            for item in result[category]['items']:
                if category == 'tracks':
                    artist = item['album']['artists'][0]['name']
                    title = item['name']
                    album = item['album']['name']
                    print(f'{title} by {artist} from the album {album}')
                elif category == 'albums':
                    artist = item['artists'][0]['name']
                    album = item['name']
                    print(f'{album} by {artist}')
                elif category == 'artists':
                    artist = item['name']
                    print(f'{artist}')
    else:
        category = input_decider(choice)
        print(f"\n{category.capitalize()}\n{'-'*76}\n")
        for item in result[category]['items']:
            if category == 'track':
                artist = item['album']['artists'][0]['name']
                title = item['name']
                album = item['album']['name']
                print(f'{title} by {artist} from the album {album}')
            elif category == 'album':
                artist = item['artists'][0]['name']
                album = item['name']
                print(f'{album} by {artist}')
            elif category == 'artist':
                artist = item['name']
                print(f'{artist}')

    # Continue or exit loop
    restart = input("\n\nWould you like to search again? y/n?\n")
    if restart.lower() != "y":
        break