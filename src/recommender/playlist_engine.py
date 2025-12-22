from typing import Dict, List
from src.api.spotify_client import SpotifyClient

class PlaylistEngine:
    """
    Uses Spotify recommendations + optional mood mapping to create a "playlist result".
    """
    def __init__(self, sp: SpotifyClient):
        self.sp = sp

    def build(self, seed_genre: str, mood: str, limit: int = 12):
        # Simple mapping; we'll improve this later
        mood_targets: Dict[str, Dict] = {
            "energetic": {"target_energy": 0.85, "target_danceability": 0.75, "target_valence": 0.65},
            "happy": {"target_valence": 0.8, "target_energy": 0.7},
            "calm": {"target_energy": 0.25, "target_valence": 0.55},
            "neutral": {},
        }
        target = mood_targets.get(mood, {})
        tracks = self.sp.recommend_tracks([seed_genre], limit=limit, target=target)
        return tracks
