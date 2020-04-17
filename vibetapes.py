import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import re
import random
import json
import requests


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
		if choice == 'Happy':
			danceability = 0.8
			tempo = 85
			valence = 1.0
			energy = 0.8
		elif choice == 'Chill':
			danceability = 0.6
			tempo = 65
			valence = 0.5
			energy = 0.5
		elif choice == 'Mellow':
			danceability = 0.3
			tempo = 35
			valence = 0.2
			energy = 0.3
		elif choice == "Productive":
			danceability = 0.3
			tempo = 45
			valence = 0.5
			energy = 0.3
		else:
			print("That wasn't a choice")
   #GETS A LIST OF THE USERS TOP ARTISTS
	def aggregate_top_artists(sp):
	    print('...getting your top artists')
	    top_artists_name = []
	    top_artists_uri = []
	    ranges = ['short_term', 'medium_term', 'long_term']
	    for r in ranges:
		top_artists_all_data = sp.current_user_top_artists(limit=10, time_range=r)
		top_artists_data = top_artists_all_data['items']
		for artist_data in top_artists_data:
		    if (artist_data["name"] not in top_artists_name):
			top_artists_name.append(artist_data['name'])
			top_artists_uri.append(artist_data['uri'])
			top_genres.append(artist_data["genres"])
	    random.shuffle(top_artists_uri)
	    return top_artists_uri

	#GETS A LIST OF THE TOP TRACKS FROM THE USERS TOP ARTISTS
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

	#ITERATES THROUGH THE TOP GENRES OF THE USRE"S TOP ARTISTS
	def get_one_genre():
	    selected_genre = []
	    for genres in top_genres:
		for single in genres:
		    selected_genre.append(single)
	    print(selected_genre)
	    return selected_genre


	#CREATES A LIST OF RECOMMENDED TRACKS BASED ON THE USERS TOP ARTISTS, TOP SONGS, AND TOP GENRES
	def recommend_tracks(sp, top_artists_uri, limit, top_tracks_uri, selected_genre):
	    print('...recommending songs')
	    lim = int(math.ceil(limit/2))
	    uris = []
	    selected_tracks = []
	    min_genre_bounds = random.randint(0,len(selected_genre))
	    min1_genre_bounds = random.randint(min_genre_bounds,len(selected_genre))
	    print("Your first genre is :"+ str(selected_genre[min_genre_bounds:min_genre_bounds+1]))
	    print("Your second genre is :"+ str(selected_genre[min1_genre_bounds:min1_genre_bounds+1]))
	    query = (sp.recommendations(seed_artists=top_artists_uri[:1], seed_genres=selected_genre[min_genre_bounds:1+min_genre_bounds],seed_tracks=top_tracks_uri[:1],
			 limit=lim, target_danceability=danceability, target_valence=valence, target_tempo=tempo, target_energy=energy))
	    query2 = (sp.recommendations(seed_artists=top_artists_uri[1:2], seed_genres=selected_genre[min1_genre_bounds:min1_genre_bounds+1],  seed_tracks=top_tracks_uri[1:2],
			 limit=lim, target_danceability=danceability, target_valence=valence, target_tempo=tempo, target_energy=energy))
	    for i, j in enumerate(query['tracks']):
		uris.append(j['uri'])
		print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")
	    for i, j in enumerate(query2['tracks']):
		uris.append(j['uri'])
		print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")

	    uris = list(set(uris))
	    return uris
	#FINALLY CREATES THE PLAYLIST AND ADDS THE RECOMMENDED SONGS FROM RECOMMEND_TRACKS
	def create_playlist(sp, selected_tracks_uri, limit, playlist_title, playlist_description):
	    print('...creating playlist')
	    user_all_data = sp.current_user()
	    user_id = user_all_data["id"]

	    playlist_all_data = sp.user_playlist_create(user_id, playlist_title, description=playlist_description)
	    playlist_id = playlist_all_data["id"]
	    playlist_uri = playlist_all_data["uri"]

	    random.shuffle(selected_tracks_uri)
	    sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri[0:limit])
	    return playlist_uri




else:
    print("Can't get token for", username)

