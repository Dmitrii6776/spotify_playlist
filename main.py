import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input('Which year do you want to travel to? Type a year in this format YYYY-MM-DD: ')
spotify_client_id = "CLIENT_ID"
spotify_token = "TOKEN"
spotify_redirect_uri = "http://example.com"
spotify_scope = "playlist-modify-private"

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
yc_web_page = response.text
music_list = []

soup = BeautifulSoup(yc_web_page, "html.parser")
articles = soup.findAll("span", class_="chart-element__information__song text--truncate color--primary")
for article in articles:
    music_list.append(article.getText())

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               redirect_uri="http://example.com",
                                               client_id=spotify_client_id,
                                               client_secret=spotify_token,
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]
print(user_id)
sp_songs_uri = []
year = date.split("-")[0]
for song in music_list:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        sp_songs_uri.append(uri)
    except Exception:
        print(f"{song} doesn't exist. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=sp_songs_uri)

