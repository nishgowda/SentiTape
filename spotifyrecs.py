

import requests
import json
import re
import spotipy
import spotipy.util as util

# SETTINGS

client_id = "2e24f089043f4ca99454eacc470d9ec8"
client_secret = "3b266e93c2f8433fb22ce651c8161ca6"
redirect_uri = "http://localhost:3000/"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
endpoint_url = "https://api.spotify.com/v1/recommendations?"

user_id = input("Enter your spotify ID:  ")
token = util.prompt_for_user_token(user_id, scope, client_id, client_secret, redirect_uri)

if token:
  uris = []
  def authenticate_spotify():
    print('...connecting to Spotify')
    sp = spotipy.Spotify(auth=token)
    return sp
  def getTracks():
    genres = {
    1 : "pop",
    2 : "dance pop",
    3 : "rap",
    4 : "post-teen pop",
    5 : "pop rap",
    6 : "rock",
    7 : "latin",
    8 : "hip hop",
    9 : "trap",
    10  : "modern rock",
    11  : "tropical house",
    12  : "reggaeton",
    13  : "edm",
    14  : "melodic rap",
    15  : "pop rock",
    16  : "latin pop",
    17  : "electropop",
    18  : "classic rock",
    19  : "album rock",
    20  : "mellow gold"
    }
    # OUR FILTERS
    limit =int(input("How many songs do you want in your playlist?  "))
    market="US"
    print("Available Genres: ")
    for x in genres:
      print(genres[x])
    seed_genres=input("What genre music do you want?  ")
    target_danceability=float(input("How danceable do you want your music to be? (0.0-1.0) "))
    energy_level = float(input("How energetic do you want the music to be? (0.0-1.0)  "))
    popularity = int(input("How popular should the music be? (0-100)  "))
     
    artist_token = input('Enter the artist token of a song:  ')
    seed_artists = re.sub("spotify:artist:", "", str(artist_token))
    track_token = input('Enter the track token of a song:  ')
    seed_tracks = re.sub("spotify:track:", "", str(track_token))
  # PERFORM THE QUERY
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}&energy_level={energy_level}&popularity={popularity}'
    query += f'&seed_artists={seed_artists}'
    query += f'&seed_tracks={seed_tracks}'

    response = requests.get(query,
                   headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})
    json_response = response.json()

    print('Recommended Songs:')
    for i,j in enumerate(json_response['tracks']):
                uris.append(j['uri'])
                print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")
  def getPlaylist():
    playlist_title = input('Enter a title for your playlist:  ')
    playlist_description = input('Enter a description for your playlist:  ')
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    request_body = json.dumps({
              "name": playlist_title,
              "description": playlist_description,
              "public": True
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})

    url = response.json()['external_urls']['spotify']
    ##print(response.status_code)

    playlist_id = response.json()['id']

    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    request_body = json.dumps({
              "uris" : uris
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})
    ##print(response.status_code) 
    print(f'Your playlist is ready at {url}')

  spotify_auth = authenticate_spotify()
  getTracks()
  getPlaylist()
else:
  print('token not found')


