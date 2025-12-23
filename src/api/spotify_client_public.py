import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Dict

from src.secrets.spotify_keys import CLIENT_ID, CLIENT_SECRET


class SpotifyClientPublic:
    """
    Public / guest Spotify client.
    No login. No playlist creation.
    Search-only access.
    """

    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(auth_manager=auth)

    # ---------------------------
    # Artists by genre
    # ---------------------------
    def get_artists_from_genre(self, genre: str, limit: int = 6) -> List[Dict]:
        results = self.sp.search(
            q=f"genre:{genre}",
            type="artist",
            limit=limit
        ) or {}

        items = results.get("artists", {}).get("items", [])
        artists: List[Dict] = []

        for a in items:
            images = a.get("images", [])
            artists.append({
                "name": a.get("name"),
                "url": a.get("external_urls", {}).get("spotify"),
                "image": images[0]["url"] if images else None,
                "genres": a.get("genres", [])
            })

        return artists

    # ---------------------------
    # Tracks by genre
    # ---------------------------
    def get_tracks_from_genre(self, genre: str, limit: int = 8) -> List[Dict]:
        results = self.sp.search(
            q=f"genre:{genre}",
            type="track",
            limit=limit
        ) or {}

        items = results.get("tracks", {}).get("items", [])
        tracks: List[Dict] = []

        for t in items:
            album = t.get("album", {})
            images = album.get("images", [])
            artists = t.get("artists", [])

            tracks.append({
                "id": t.get("id"),
                "title": t.get("name"),
                "artist": artists[0]["name"] if artists else "Unknown",
                "url": t.get("external_urls", {}).get("spotify"),
                "preview": t.get("preview_url"),
                "cover": images[0]["url"] if images else None,
            })

        return tracks

    # ---------------------------
    # Playlists by genre (search)
    # ---------------------------
    def playlists_for_genre(self, genre: str, limit: int = 8) -> List[Dict]:
        results = self.sp.search(
            q=genre,
            type="playlist",
            limit=limit
        ) or {}

        items = results.get("playlists", {}).get("items", [])
        playlists: List[Dict] = []

        for p in items:
            # Skip None items
            if p is None:
                continue
                
            images = p.get("images", [])
            playlists.append({
                "name": p.get("name"),
                "url": p.get("external_urls", {}).get("spotify"),
                "image": images[0]["url"] if images else None,
                "owner": p.get("owner", {}).get("display_name", ""),
            })

        return playlists
    # ---------------------------
    # Albums by genre
    # ---------------------------
    def get_albums_from_genre(self, genre: str, limit: int = 8) -> List[Dict]:
        results = self.sp.search(
            q=f"genre:{genre}",
            type="album",
            limit=limit
        ) or {}

        items = results.get("albums", {}).get("items", [])
        albums: List[Dict] = []

        for a in items:
            if a is None:
                continue
                
            images = a.get("images", [])
            artists = a.get("artists", [])
            
            albums.append({
                "name": a.get("name"),
                "artist": artists[0]["name"] if artists else "Unknown",
                "url": a.get("external_urls", {}).get("spotify"),
                "image": images[0]["url"] if images else None,
                "release_date": a.get("release_date"),
                "total_tracks": a.get("total_tracks", 0),
            })

        return albums