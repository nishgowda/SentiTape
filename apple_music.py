import applemusicpy
import requests

secret_key = """-----BEGIN PRIVATE KEY-----

-----END PRIVATE KEY-----"""
key_id = '9XSZP7A749'
team_id = 'GCBWVTCRDA'

am = applemusicpy.AppleMusic(secret_key, key_id, team_id)
results = am.search('travis scott', types=['albums'], limit=5)

for item in results['results']['albums']['data']:
    print(item['attributes']['name'])



#username = 
#endpoint_url = "https://api.music.apple.com/v1/{username}/library/playlists"

top_charts = am.charts(types=['songs'],limit=20)
for songs in top_charts['results']['songs'][0]['data']:
	print(songs['attributes']['name'] + " by " + songs['attributes']['artistName'])
