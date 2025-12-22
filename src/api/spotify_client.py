import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.secrets.spotify_keys import CLIENT_ID, CLIENT_SECRET

class SpotifyClient:
    """
    Uses Client Credentials flow: good for public search/recommendations.
    No user login required.
    """
    def __init__(self):
        auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=auth)

    def available_seed_genres(self):
        feats = self.sp.audio_features(tracks=track_ids)
        return [f for f in feats if f is not None]

    def get_artists_from_genre(self, genre: str, limit: int = 6):
        results = self.sp.search(q=f"genre:{genre}", type="artist", limit=limit)
        out = []
        for a in results["artists"]["items"]:
            out.append({
                "name": a["name"],
                "url": a["external_urls"]["spotify"],
                "image": a["images"][0]["url"] if a.get("images") else None,
                "genres": a.get("genres", []),
            })
        return out

    def get_tracks_from_genre(self, genre: str, limit: int = 8):
        results = self.sp.search(q=f"genre:{genre}", type="track", limit=limit)
        tracks = []

        for t in results["tracks"]["items"]:
            album = t.get("album")
            images = album.get("images") if album else []

            tracks.append({
                "title": t.get("name"),
                "artist": t["artists"][0]["name"] if t.get("artists") else "Unknown",
                "preview": t.get("preview_url"),
                "url": t["external_urls"]["spotify"],
                "cover": images[0]["url"] if images else None,
                "id": t.get("id"),
            })
        return tracks


    def recommend_tracks(self, seed_genres: list[str], limit: int = 10, target: dict | None = None):
        """
        Spotify recommendations endpoint. 'target' can include target_energy, target_valence, etc.
        """
        target = target or {}
        rec = self.sp.recommendations(seed_genres=seed_genres, limit=limit, **target)
        return rec["tracks"]

    def related_artists(self, artist_id: str):
        results = self.sp.artist_related_artists(artist_id)
        out = []
        for a in results["artists"]:
            out.append({
                "name": a["name"],
                "url": a["external_urls"]["spotify"],
                "image": a["images"][0]["url"] if a.get("images") else None,
                "id": a["id"],
            })
        return out

    def playlists_for_genre(self, genre: str, limit: int = 8):
        results = self.sp.search(q=f"{genre}", type="playlist", limit=limit)
        out = []
        for p in results["playlists"]["items"]:
            out.append({
                "name": p["name"],
                "url": p["external_urls"]["spotify"],
                "image": p["images"][0]["url"] if p.get("images") else None,
                "owner": p["owner"]["display_name"] if p.get("owner") else "",
            })
        return out

    def audio_features(self, track_ids: list[str]):
        """
        Returns Spotify audio features like energy, danceability, valence, etc.
        """
        feats = self.sp.audio_features(tracks=track_ids)
        return [f for f in feats if f is not None]
