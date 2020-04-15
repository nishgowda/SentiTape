
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import re
import random
import json
import requests
# - Steps:
#     - 1. Authenticating Spotipy (✅)
#     - 2. Creating a list of your favorite artists (get max 50) ✅)
#         - API: Get a User’s Top Artists and Tracks
#         - Scope: user-top-read
#     - 3. For each of the artists, get all tracks for each artist. ✅
#         - API: Get an Artist’s Top Tracks
#     - 4. From top tracks, select tracks that are within a certain valence range ✅
#         - API: Get Audio Features for Several Tracks
#     - 5. From these tracks, create a playlist for user ✅
#         - API: Create a Playlist
#         - API: Add Tracks to a Playlist
#         - Scope: playlist-modify-public

client_id = "blank"
client_secret = "blank"
redirect_uri = "blank"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

danceability = 0.0
tempo = 0.0
valence = 0.0
energy = 0.0

token = util.prompt_for_user_token(
    username, scope, client_id, client_secret, redirect_uri)

if token:

	# Step 1. Authenticating Spotipy

	def authenticate_spotify():
		print('...connecting to Spotify')
		sp = spotipy.Spotify(auth=token)
		return sp

	def type_of_playlist(choice):
		global danceability
		global energy
		global tempo
		global valence
		if choice == 'Pumped':
			danceability = 0.9
			tempo = 115
			valence = 0.9
			energy = 0.9
		elif choice == 'Chill':
			danceability = 0.6
			tempo = 65
			valence = 0.5
			energy = 0.5
		elif choice == "Productive":
			danceability = 0.3
			tempo = 45
			valence = 0.5
			energy = 0.3
		else:
			print("That wasn't a choice")
    # Step 2. Creating a list of your favorite artists

	def aggregate_top_artists(sp, genres):
		print('...getting your top artists')
		top_artists_name = []
		top_artists_uri = []

		ranges = ['short_term', 'medium_term', 'long_term']
		for r in ranges:
			top_artists_all_data = sp.current_user_top_artists(limit=100, time_range=r)
			top_artists_data = top_artists_all_data['items']
			for artist_data in top_artists_data:
				if (artist_data["name"] not in top_artists_name):
					top_artists_name.append(artist_data['name'])
					top_artists_uri.append(artist_data['uri'])
					if (genres not in artist_data["genres"]):
						top_artists_uri.remove(artist_data['uri'])
		random.shuffle(top_artists_uri)
		return top_artists_uri

    # Step 3. For each of the artists, get a set of tracks for each artist

	def aggregate_top_tracks(sp, top_artists_uri):
		print("...getting top tracks")
		top_tracks_uri = []
		for artist in top_artists_uri:
			top_tracks_all_data = sp.artist_top_tracks(artist)
			top_tracks_data = top_tracks_all_data['tracks']
			for track_data in top_tracks_data:
				top_tracks_uri.append(track_data['uri'])
		random.shuffle(top_tracks_uri)
		return top_tracks_uri

	# Step 4. From top tracks, select tracks that are within a certain mood range
	def recommend_tracks(sp, top_artists_uri, genres,top_tracks_uri):
		print("...recommending songs")
		endpoint_url = "https://api.spotify.com/v1/recommendations?"
		market = "US"
		lim = int(100/4)
		uris = []
		query = (sp.recommendations(seed_artists=top_artists_uri[:1],seed_genres=genres, seed_tracks=top_tracks_uri[:1], limit = lim, target_danceability=danceability, target_valence = valence, target_tempo=tempo, target_energy=energy))
		query1 = (sp.recommendations(seed_artists=top_artists_uri[1:2],seed_genres=genres, seed_tracks=top_tracks_uri[1:2], limit = lim, target_danceability=danceability, target_valence = valence, target_tempo=tempo, target_energy=energy))
		for i, j in enumerate(query['tracks']):
			uris.append(j['uri'])
			print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")
		for i, j in enumerate(query1['tracks']):
			uris.append(j['uri'])
			print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")
		return uris		

	# Step 5. From these tracks, create a playlist for user

	def create_playlist(sp, selected_tracks_uri, limit, choice, playlist_title, playlist_description):

		print("...creating playlist")
		user_all_data = sp.current_user()
		user_id = user_all_data["id"]

		playlist_all_data = sp.user_playlist_create(user_id, playlist_title, description=playlist_description)
		playlist_id = playlist_all_data["id"]

		random.shuffle(selected_tracks_uri)
		sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri[0:limit])

	print("What is your vibe? ")
	choice = input('')
	limit  = int(input('How many songs do you want? '))
	genres = input("What genre music do you want? ")
	playlist_title = input("Playlist title: ")
	playlist_description = input("playlist description: ")
	type_of_playlist(choice)
	spotify_auth = authenticate_spotify()
	top_artists = aggregate_top_artists(spotify_auth, genres)
	top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
	recommends = recommend_tracks(spotify_auth, top_artists, genres, top_tracks)
	#selected_tracks = select_tracks(spotify_auth, recommends)
	create_playlist(spotify_auth, recommends,limit,choice, playlist_title, playlist_description)



else:
    print("Can't get token for", username)

