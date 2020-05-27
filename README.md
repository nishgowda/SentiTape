# Vibetape

### What is it?

Have you ever had a good idea for the perfect playlist but are just too lazy to make one? Vibetape is the perfect combination of program automation and user control as it gives users the abilitiy to customize the atrributes of their playlists while saving them the time of sitting down and ardiously adding songs to a playlist.

Vibetape prompts the user to choose from an array of moods that they might be feeling at a given moment and then will traverse through the users most played artist and his or her most played songs and uses that data along with the users "vibe" to generate a list of recommendations. The algorithm then creates a playlists titled whatever the user desires (along with a description) and then adds the recommended songs to that playlist.

**Dependencies:**
- Spotipy--python library for the Spotify web api: 
```pip install spotipy3```
- Flask--server side library for python:  
```pip install Flask```
- Must create a spotify app on their developer page. Change the CLIENT ID, CLIENT SECRET, and REDIRECT URI on main.py

**How to run:**
- Once requirments/dependicies are installed, simply run:
```python3 main.py```
- Visit```localhost:5000```on webrowser

### The Tech Stack:

**Authentication/Security:**
  - Flask Web Sessions
  - Spotify Oauth Tokens - CLIENT ID, CLIENT SECRET, REDERICT URI, SCOPE (Learn about this at: https://developer.spotify.com/documentation/general/guides/authorization-guide/)

**Back End:**
  - Python
  - Flask Microservice

**Front End:**
  - Jinja2 (Used with Flask)
  - HTML5
  - CSS3
  - Javascript
  
**TO DO:**
  - [X] Reconfigure index.html, Table View etc.
  - [X] Fix bug with displaying users songs in check view
  - [X] Fix bug with duplicate POST request on refresh
  - [ ] Get server hosted (Heroku, Google App Engine, AWS)
  - [X] Decide if database is needed (it's not -- Spotify secures user data; merely retrieving it)
  - [X] \(Optional) Decide if sentiment analysis should replace vibe selection


