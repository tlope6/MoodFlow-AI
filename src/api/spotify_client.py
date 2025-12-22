import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.secrets.spotify_keys import CLIENT_ID, CLIENT_SECRET
from typing import List, Dict, Optional


#all the genres from spotify
SPOTIFY_SEED_GENRES = {
    "pop", "rock", "hip-hop", "rap", "edm", "dance", "electronic",
    "jazz", "classical", "blues", "country", "metal", "indie",
    "folk", "r-n-b", "soul", "latin", "reggae", "punk",
    "house", "techno", "ambient", "alternative"
}

class SpotifyClient:
    """
    Uses Spotify Client Credentials flow.
    Safe handling of optional Spotify fields.
    """


    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(auth_manager=auth)

    # # ---------------------------
    # # Seed genres
    # # ---------------------------
    # def available_seed_genres(self) -> List[str]:
    #     response = self.sp.recommendation_genre_seeds()
    #     return response.get("genres", []) if response else []

    # ---------------------------
    # Artists by genre
    # ---------------------------
    def get_artists_from_genre(self, genre: str, limit: int = 6) -> List[Dict]:
        results = self.sp.search(q=f"genre:{genre}", type="artist", limit=limit) or {}
        items = results.get("artists", {}).get("items", [])

        artists = []
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
        results = self.sp.search(q=f"genre:{genre}", type="track", limit=limit) or {}
        items = results.get("tracks", {}).get("items", [])

        tracks = []
        for t in items:
            album = t.get("album", {})
            images = album.get("images", [])

            tracks.append({
                "id": t.get("id"),
                "title": t.get("name"),
                "artist": t["artists"][0]["name"] if t.get("artists") else "Unknown",
                "preview": t.get("preview_url"),
                "url": t.get("external_urls", {}).get("spotify"),
                "cover": images[0]["url"] if images else None
            })
        return tracks

    # ---------------------------
    # Recommendations
    # ---------------------------
    def recommend_tracks(
        self,
        seed_genres: List[str],
        limit: int = 10,
        target: Optional[Dict] = None
    ) -> List[Dict]:
        target = target or {}
        rec = self.sp.recommendations(seed_genres=seed_genres, limit=limit, **target)
        return rec.get("tracks", []) if rec else []

    # ---------------------------
    # Related artists
    # ---------------------------
    def related_artists(self, artist_id: str) -> List[Dict]:
        results = self.sp.artist_related_artists(artist_id) or {}
        artists = results.get("artists", [])

        out = []
        for a in artists:
            images = a.get("images", [])
            out.append({
                "name": a.get("name"),
                "url": a.get("external_urls", {}).get("spotify"),
                "image": images[0]["url"] if images else None,
                "id": a.get("id"),
            })
        return out

    # ---------------------------
    # Playlists
    # ---------------------------
    def playlists_for_genre(self, genre: str, limit: int = 8) -> List[Dict]:
        results = self.sp.search(q=genre, type="playlist", limit=limit) or {}
        items = results.get("playlists", {}).get("items", [])

        playlists = []
        for p in items:
            images = p.get("images", [])
            playlists.append({
                "name": p.get("name"),
                "url": p.get("external_urls", {}).get("spotify"),
                "image": images[0]["url"] if images else None,
                "owner": p.get("owner", {}).get("display_name", ""),
            })
        return playlists

    # ---------------------------
    # Audio features
    # ---------------------------
    def audio_features(self, track_ids: List[str]) -> List[Dict]:
        if not track_ids:
            return []

        feats = self.sp.audio_features(tracks=track_ids) or []
        return [f for f in feats if f is not None]
