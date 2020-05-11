import requests
import json
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import random
import math

danceability = 0.0
tempo = 0.0
valence = 0.0
energy = 0.0
top_genres = []
lim = 0
recs = []
playlist_id = []


def type_of_playlist(mood, prob):
    global danceability
    global energy
    global tempo
    global valence
    print('Mood is: ')
    if prob <= 0.4 and mood=='Negative':
        print('Chill')
        danceability += 0.6
        energy += 0.5
        tempo += 65.0
        valence += 0.5
    if prob > 0.3 and prob <= 0.4 and mood=='Positive':
        print('productive')
        danceability += 0.2
        energy += 0.3
        tempo += 45.0
        valence += 0.4     
    elif prob >= 0.5 and prob <= 0.8 and mood=='Positive':
        print('happy')
        danceability += 0.8
        tempo += 95
        valence += 1.0
        energy += 0.9
    elif prob > 0.6 and prob <= 0.8 and mood=='Negative':
        print('mellow')
        danceability += 0.8
        tempo += 95
        valence += 1.0
        energy += 0.9
    elif prob > 0.8 and mood=='Positive':
        print('pumped')
        danceability += 0.9
        energy += 0.9
        tempo += 115.0
        valence += 0.8
    else:
        print('doing else')
        danceability += 0.5
        energy += 0.5
        tempo += 85.0
        valence += 0.5
        
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
    random.shuffle(top_artists_name)
    print("Your first artist is: " + str(top_artists_name[:1]))
    print("Your second artist is: " + str(top_artists_name[1:2]))
    top_tracks = sp.current_user_saved_tracks()
    print('number of saved tracks' +str((top_tracks['total'])))
    return top_artists_uri

def get_playlists(sp):
    playlists = sp.current_user_playlists()
    count = 0
    for x in playlists:
        if isinstance(playlists[x], list):
            count+= len(playlists[x])
    return count

def saved_tracks(sp):
    tracks = sp.current_user_saved_tracks()
    count = 0
    for x in tracks:
        if isinstance(tracks[x], list):
            count+= len(tracks[x])
    return count

def saved_albums(sp):
    albums = sp.current_user_saved_albums()
    count = 0
    for x in albums:
        if isinstance(albums[x], list):
            count += len(albums[x])
    return count

def followed_artists(sp, range, limit):
    top_artists_name = []
    if range == 'Short Term':
        newRange = 'short_term'
    elif range == 'Medium Term':
        newRange = 'medium_term'
    elif range == 'Long Term':
        newRange = 'long_term'
    ranges = [newRange]
    for r in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=limit, time_range=r)
        top_artists_data = top_artists_all_data['items']
        for artist_data in top_artists_data:
            if (artist_data["name"] not in top_artists_name):
                top_artists_name.append(artist_data['name'])
                top_genres.append(artist_data["genres"])
    return (top_artists_name)

def most_played_songs(sp, range, limit):
    top_track_name = []
    top_track_artist = []
    if range == 'Short Term':
        newRange = 'short_term'
    elif range == 'Medium Term':
        newRange = 'medium_term'
    elif range == 'Long Term':
        newRange = 'long_term'
    ranges = [newRange]
    
    for r in ranges:
        top_track_all_data = sp.current_user_top_tracks(limit=limit, time_range=r)
        top_track_data = top_track_all_data['items']
        for track_data in top_track_data:
            if track_data["name"] not in top_track_name:
                strang = ""
                strang+=str(track_data['name'])
                strang+=str(" by ")
                strang+=str(track_data['artists'][0]['name'])
                top_track_name.append(strang)
    return top_track_name

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

def following(sp):
    top_artists_name = []
    followed_artists_all_data = sp.current_user_followed_artists(limit=50)
    followed_artists_data = (followed_artists_all_data['artists'])
    for artist_data in followed_artists_data["items"]:
        if artist_data["name"] not in top_artists_name:
            top_artists_name.append(artist_data['name'])
    return len(top_artists_name)
#ITERATES THROUGH THE TOP GENRES OF THE USRE"S TOP ARTISTS
def get_one_genre():
    selected_genre = []
    for genres in top_genres:
        for single in genres:
            selected_genre.append(single)
    return selected_genre


#CREATES A LIST OF RECOMMENDED TRACKS BASED ON THE USERS TOP ARTISTS, TOP SONGS, AND TOP GENRES
def recommend_tracks(sp, top_artists_uri, limit, top_tracks_uri, selected_genre):
    print('...recommending songs')
    global lim
    global recs
    lim = int(math.ceil(limit/2))
    uris = []
    selected_tracks = []
    fixed_songs = []
    min_genre_bounds = random.randint(0,len(selected_genre))
    min1_genre_bounds = random.randint(min_genre_bounds,len(selected_genre))
    print("Your first genre is :"+ str(selected_genre[min_genre_bounds:min_genre_bounds+1]))
    print("Your second genre is :"+ str(selected_genre[min1_genre_bounds:min1_genre_bounds+1]))

    query = (sp.recommendations(seed_artists=top_artists_uri[:1], seed_genres=selected_genre[min_genre_bounds:1+min_genre_bounds],seed_tracks=top_tracks_uri[:1],
	         limit=lim, target_danceability=danceability, target_valence=valence, target_tempo=tempo, target_energy=energy))
    query2 = (sp.recommendations(seed_artists=top_artists_uri[1:2], seed_genres=selected_genre[min1_genre_bounds:min1_genre_bounds+1],  seed_tracks=top_tracks_uri[1:2],
	         limit=lim, target_danceability=danceability, target_valence=valence, target_tempo=tempo, target_energy=energy))
    for song in query['tracks']:
        uris.append(song['uri'])
        fixed_songs.append(f"{song['name']}\" by {song['artists'][0]['name']}")
    for track in query2['tracks']:
        uris.append(track['uri'])
        fixed_songs.append(f"{track['name']}\" by {track['artists'][0]['name']}")

    ## REMOVE DUPLICATE SONGS FROM PLAYLIST AND REPLACE THEM WITH NEW ONES
    ## ALSO POPS ANY SONGS FROM URIS IF THE LIST LENGTH IS BIGGER THAN LIMIT (CAUSED BY AN ISSUE WITH RECCOMEDATIONS)
    res = []
    for i in uris:
        if i not in res:
            res.append(i)
    for x in fixed_songs:
        if x not in recs:
            recs.append(x)
    while(len(res)<limit):
        print('..res too small limit')
        print(len(res))
        sub = int((limit-len(res)) + 1)
        print(sub)
        query3 = (sp.recommendations(seed_artists=top_artists_uri[:1], seed_genres=selected_genre[min_genre_bounds:1+min_genre_bounds],seed_tracks=top_tracks_uri[:1],
	         limit=sub, target_danceability=danceability, target_valence=valence, target_tempo=tempo, target_energy=energy))
        for piece in query3["tracks"]:
            res.append(piece["uri"])
            recs.append(f"{piece['name']}\" by {piece['artists'][0]['name']}")
            break
    if(len(res) > limit):
        print('..res too big')
        diff = (len(res)-limit)
        res.pop(diff)
        recs.pop(diff)

    for i,j in enumerate(recs):
        print(f"{i+1}) \"{j}")
    return res

def display_recommendation_songs():
    global recs
    return recs
    del recs

#FINALLY CREATES THE PLAYLIST AND ADDS THE RECOMMENDED SONGS FROM RECOMMEND_TRACKS
def create_playlist(sp, selected_tracks_uri, limit, playlist_title, playlist_description):
    print('...creating playlist')
    user_all_data = sp.current_user()
    user_id = user_all_data["id"]
    global playlist_id
    playlist_all_data = sp.user_playlist_create(user_id, playlist_title, description=playlist_description)
    playlist_id = playlist_all_data["id"]
    playlist_uri = playlist_all_data["uri"]

    sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri[0:limit])
    
    return playlist_uri
def retrieve_playlist_cover(sp):
    user_all_data = sp.current_user()
    user_id = user_all_data["id"]

    playlist_cover = sp.playlist_cover_image(playlist_id)
    return playlist_cover[0]["url"]