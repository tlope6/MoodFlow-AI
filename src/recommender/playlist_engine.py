from typing import List, Dict, Optional
# from src.recommender.ranker import track_distance
from src.api.spotify_genres import SPOTIFY_SEED_GENRES  

class PlaylistEngine:
    def __init__(self, sp_user):
        self.sp = sp_user

    def recommend_ranked(self, genre: str, mood: Optional[str] = None, seed_track_ids: Optional[List[str]] = None, limit: int = 10) -> List[Dict]:
        """
        Get track recommendations based on genre or seed track
        Note: mood parameter is ignored since audio features API is deprecated
        """
        genre = genre if genre in SPOTIFY_SEED_GENRES else "pop"

        # Get candidates from Spotify
        # If user provided a seed track, use that; otherwise use genre
        tracks = self.sp.recommend_tracks(
            seed_genres=[genre] if not seed_track_ids else None,
            seed_tracks=seed_track_ids,
            limit=limit
        )

        if not tracks:
            return []
        
        # Return simplified format (no audio features or distance scoring)
        return [{"track": t} for t in tracks]