from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from src.secrets.spotify_keys import CLIENT_ID, CLIENT_SECRET

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=auth_manager)

result = sp.search(q="genre:rock", type="track", limit=1)
print(result)


# def test_placeholder() :
#     assert True