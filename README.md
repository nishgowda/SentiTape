# Vibetape

### What is it?

Have you ever had a good idea for the perfect playlist but are just too lazy to make one? Vibetape is the perfect combination of program automation and user control as it gives users the abilitiy to customize the atrributes of their playlists while saving them the time of sitting down and ardiously adding songs to a playlist.

Vibetape propmpts the user to choose from an array of moods that they might be feeling at a given moment and then will traverse through the users most played artist and his or her most played songs and uses that data along with the users "vibe" to generate a list of recommendations. The algorithm then creates a playlists titled whatever the user desires (along with a description) and then adds the recommended songs to that playlist.

**Requirments:**
- Spotipyg, python library for the Spotify web api: pip install spotipy3
- Flask, server side library for python:  pip install Flask
- Must create a spotify app on their developer page. Change the CLIENT ID, CLIENT SECRET, and REDIRECT URI on main.py

**How to run:**
- Once requirments/dependicies are installed, simply run: python3 main.py in terminal
- Visit local host on webrowser and voila!


**Authentication/Security:**
  - Flask Login
  - Spotify Oauth Tokens: CLIENT ID, CLIENT SECRET, REDERICT URI (Learn about this at: https://developer.spotify.com/)

**Back End:**
  - Python
  - Flask Server

**Front End:**
  - Jinja2
  - HTMl5
  - CSS3
  - Javascript
  
**TO DO:**
  - [ ] Reconfigure index.html, Table View etc.
  - [ ] Get server hosted (Heroku, Google App Engine)
  - [X] Decide if database is needed (it's not -- Spotify secures user data; merely retrieving data)
  - [ ] \(Optional) decide if sentiment analysis should replace vibe selection


