from flask import Flask, render_template, redirect, request, session, make_response, session, redirect, url_for
import spotipy
import spotipy.util as util
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import os
from vibetape_functions import retrieve_playlist_cover,display_recommendation_songs,get_one_genre,most_played_songs,followed_artists,type_of_playlist, aggregate_top_artists,saved_albums , saved_tracks,get_playlists ,following,get_one_genre, aggregate_top_tracks, recommend_tracks, create_playlist
app = Flask(__name__)

app.secret_key = str(os.urandom(24))

API_BASE = 'https://accounts.spotify.com'

# Make sure you add this to Redirect URIs in the setting of the application dashboard
REDIRECT_URI = "RED_URI

SCOPE = 'user-library-read user-top-read playlist-modify-public user-follow-read'
CLI_ID = "CLI_ID"
CLI_SEC = 'CLI_SEC'

# Set this to True for testing but you probably want it set to False in production.
SHOW_DIALOG = True

# Log in variable that updates when the user is logged in via Ouath Authenitication
is_logged_in = False
reqs = False
# GLOBAL VARIABLES
limit = 0
choice = ""
playlist_title = ''
playlist_description = ''
selected_songs = []
recs = []
playlist = []
playlist_cover = []

# authorization-code-flow Step 1. Have your application request authorization;
# the user logs in and authorizes access
@app.route("/verify")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)

# Home page, user must log in
@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        return redirect(url_for('verify'))

    return render_template("home.html")

# App route to the Index page
# User must be logged into spotify, else redirected to home page
@app.route("/index")
def index():
    global reqs
    if is_logged_in == True:
        reqs = True
        sp = spotipy.Spotify(auth=session['toke'])
        user_all_data = sp.current_user()
        user_id = user_all_data["display_name"]
        top_artists = following(sp)
        followers = user_all_data["followers"]["total"]
        friends = followers + top_artists
        num_playlists = get_playlists(sp)
        top_tracks = sp.current_user_saved_tracks()
        num_tracks = int(top_tracks['total'])
        top_albums = sp.current_user_saved_albums()
        num_albums = top_albums['total']
        recs=display_recommendation_songs()
        rec_size = len(recs)
        if  not user_all_data["images"]:
            user_image = ""
        else:
            user_image = user_all_data["images"][0]["url"]
        return render_template("index.html", user_image=user_image, user_id=user_id, top_artists=top_artists, followers=followers, friends=friends, num_playlists=num_playlists, num_tracks=num_tracks, num_albums=num_albums, recs=recs)
    else:
        return redirect("/")


# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
@app.route("/api_callback")
def api_callback():
    global is_logged_in
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/api_callback",
        "client_id": CLI_ID,
        "client_secret": CLI_SEC
    })

    res_body = res.json()
    print(res.json())
    session["toke"] = res_body.get("access_token")
    is_logged_in = True # Logged in variable globally updated to allow user to acces the rest of the
    return redirect("index")

# Routes to the data page 
# User must be logged in, else redirected back to the home route
@app.route("/data", methods=['GET', 'POST'])
def user_data():
    if is_logged_in == True:
        if request.method == 'POST':
            time = request.form['time']
            limit = request.form['limit']
        else:
            time = 'Short Term'
            limit= 10
        sp = spotipy.Spotify(auth=session['toke'])
        artists = followed_artists(sp,time, limit)
        songs = most_played_songs(sp, time, limit)
        size = len(artists)
        genres = get_one_genre()
        default = time
        return render_template("data.html", top_artists=artists, songs=songs, genres=genres, default=default)
    else:
        return redirect("/")


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data


@app.route("/index", methods=['POST'])
def go():
    global limit 
    global choice
    global playlist_title
    global playlist_description
    limit = request.form['limit']
    limit = int(limit)
    choice = request.form['choice']
    playlist_title = request.form['playlist_title']
    playlist_description = request.form['playlist_description']
    return redirect('/check')




@app.route("/check")
def check():
    if is_logged_in == True:
        global selected_songs
        global recs
        sp = spotipy.Spotify(auth=session['toke'])
        type_of_playlist(choice)
        top_artists = aggregate_top_artists(sp)
        top_tracks = aggregate_top_tracks(sp, top_artists)
        selected_genre = get_one_genre()
        selected_songs = recommend_tracks(sp, top_artists, limit, top_tracks, selected_genre)
        recs = display_recommendation_songs()
        return redirect("/songs")
    else:
        return redirect("/")

@app.route("/songs")
def songs():
    if is_logged_in == True:
        global recs
        return render_template('check.html', recs=recs)
    else:
        return redirect("/")

@app.route("/songs", methods=['POST'])
def finish():
    if is_logged_in == True:
        global reqs
        global playlist
        global playlist_cover
        sp = spotipy.Spotify(auth=session['toke'])
        playlist = create_playlist(sp, selected_songs, limit, playlist_title, playlist_description)
        playlist_cover = retrieve_playlist_cover(sp)
        return redirect('/done')
    else:
        return redirect("/")

@app.route("/done")
def done():
    if is_logged_in == True:
        return render_template('playlist.html', playlist=playlist, playlist_cover=playlist_cover)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
