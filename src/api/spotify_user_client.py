import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Dict, Any, List

from src.secrets.spotify_keys import CLIENT_ID, CLIENT_SECRET


class SpotifyUserClient:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://127.0.0.1:8888/callback",
                scope=(
                    "user-read-private user-read-email "
                    "playlist-modify-private playlist-modify-public "
                    "user-library-read"  # This allows reading audio features!
                )
            )
        )   

    # ---------------------------
    # User info
    # ---------------------------
    def me(self) -> Dict[str, Any]:
        user = self.sp.me()
        if user is None:
            raise RuntimeError("Spotify user not authenticated")
        return user

    # ---------------------------
    # Recommendations
    # ---------------------------
    def recommend_tracks(self, seed_genres=None, seed_artists=None, seed_tracks=None, limit=25, target=None):
        """
        Get track recommendations using genre-specific search strategies
        """
        from src.recommender.genre_strategies import get_search_strategy, GENRE_SEED_ARTISTS
        
        # Get seed track info if provided
        seed_features = None
        artist_name = None
        genre_to_search = None
        
        if seed_tracks:
            try:
                feats = self.sp.audio_features([seed_tracks[0]])
                if feats and len(feats) > 0:
                    seed_features = feats[0]
            except:
                pass
            
            try:
                track = self.sp.track(seed_tracks[0])
                if track and 'artists' in track and track['artists']:
                    artist_id = track['artists'][0]['id']
                    artist_name = track['artists'][0]['name']
                    
                    artist = self.sp.artist(artist_id)
                    if artist and 'genres' in artist and artist['genres']:
                        genre_to_search = artist['genres'][0]
                        print(f"Found artist: {artist_name}, genre: {genre_to_search}")
            except Exception as e:
                print(f"Error getting seed track info: {e}")
        
        if not genre_to_search and seed_genres:
            genre_to_search = seed_genres[0] if isinstance(seed_genres, list) else seed_genres
        
        if not genre_to_search:
            genre_to_search = "pop"
        
        # Get the search strategy for this genre
        strategy = get_search_strategy(genre_to_search)
        print(f"Using strategy for '{genre_to_search}': {strategy}")
        
        try:
            all_tracks = []
            
            # Strategy 1: Artist-focused search (K-pop, J-pop, Latin, etc.)
            if strategy["use_artist_search"]:
                print(f"Using artist-focused search for {genre_to_search}")
                
                # Use seed artists from our curated list
                artists_to_search = []
                
                # If we have the actual artist from the uploaded song, prioritize them
                if artist_name:
                    artists_to_search.append(artist_name)
                    
                    # Get related artists for variety
                    try:
                        artist_results = self.sp.search(q=f"artist:{artist_name}", type='artist', limit=1, market='US')
                        if artist_results and 'artists' in artist_results and artist_results['artists']['items']:
                            artist_id = artist_results['artists']['items'][0]['id']
                            related = self.sp.artist_related_artists(artist_id)
                            if related and 'artists' in related:
                                artists_to_search.extend([a['name'] for a in related['artists'][:strategy["max_related_artists"]]])
                    except:
                        pass
                
                # Fall back to curated seed artists for this genre
                if len(artists_to_search) < 5:
                    artists_to_search.extend(strategy["seed_artists"][:10])
                
                # Search tracks by these artists (recent only)
                for artist in artists_to_search[:15]:  # Limit to avoid too many requests
                    try:
                        if strategy["use_year_filter"]:
                            query = f'artist:"{artist}" year:2023-2024'
                        else:
                            query = f'artist:"{artist}"'
                        
                        results = self.sp.search(q=query, type='track', limit=5, market='US')
                        if results and 'tracks' in results:
                            all_tracks.extend(results['tracks']['items'])
                    except:
                        continue
            
            # Strategy 2: Genre-based search with year filtering
            elif strategy["use_year_filter"]:
                print(f"Using time-sensitive search for {genre_to_search}")
                
                for year in [2024, 2023]:
                    results = self.sp.search(
                        q=f"genre:{genre_to_search} year:{year}",
                        type='track',
                        limit=25,
                        market='US'
                    )
                    if results and 'tracks' in results:
                        all_tracks.extend(results['tracks']['items'])
                
                # Also get related artists if we have seed track
                if artist_name:
                    try:
                        artist_results = self.sp.search(q=f"artist:{artist_name}", type='artist', limit=1, market='US')
                        if artist_results and 'artists' in artist_results and artist_results['artists']['items']:
                            artist_id = artist_results['artists']['items'][0]['id']
                            related = self.sp.artist_related_artists(artist_id)
                            if related and 'artists' in related:
                                for rel_artist in related['artists'][:5]:
                                    rel_results = self.sp.search(
                                        q=f'artist:"{rel_artist["name"]}" year:2023-2024',
                                        type='track',
                                        limit=5,
                                        market='US'
                                    )
                                    if rel_results and 'tracks' in rel_results:
                                        all_tracks.extend(rel_results['tracks']['items'])
                    except:
                        pass
            
            # Strategy 3: Standard genre search (classical, jazz, blues, etc.)
            else:
                print(f"Using standard genre search for {genre_to_search}")
                
                # Add mood keywords if available
                if strategy["mood_keywords"]:
                    for keyword in strategy["mood_keywords"]:
                        results = self.sp.search(
                            q=f"genre:{genre_to_search} {keyword}",
                            type='track',
                            limit=15,
                            market='US'
                        )
                        if results and 'tracks' in results:
                            all_tracks.extend(results['tracks']['items'])
                
                # Standard genre search
                results = self.sp.search(
                    q=f"genre:{genre_to_search}",
                    type='track',
                    limit=30,
                    market='US'
                )
                if results and 'tracks' in results:
                    all_tracks.extend(results['tracks']['items'])
                
                # Related artists if available
                if artist_name:
                    try:
                        artist_results = self.sp.search(q=f"artist:{artist_name}", type='artist', limit=1, market='US')
                        if artist_results and 'artists' in artist_results and artist_results['artists']['items']:
                            artist_id = artist_results['artists']['items'][0]['id']
                            related = self.sp.artist_related_artists(artist_id)
                            if related and 'artists' in related:
                                for rel_artist in related['artists'][:5]:
                                    rel_results = self.sp.search(
                                        q=f'artist:"{rel_artist["name"]}"',
                                        type='track',
                                        limit=5,
                                        market='US'
                                    )
                                    if rel_results and 'tracks' in rel_results:
                                        all_tracks.extend(rel_results['tracks']['items'])
                    except:
                        pass
            
            if not all_tracks:
                print(f"No search results")
                return []
            
            # Remove duplicates
            seen_ids = set()
            tracks = []
            for t in all_tracks:
                if t and t.get('id') and t['id'] not in seen_ids:
                    seen_ids.add(t['id'])
                    tracks.append(t)
            
            # Remove the seed track itself
            if seed_tracks:
                tracks = [t for t in tracks if t.get('id') != seed_tracks[0]]
            
            # Sort by popularity and recency
            tracks.sort(key=lambda x: (
                x.get('album', {}).get('release_date', '2000').startswith(('2024', '2023')),  # Recent first
                x.get('popularity', 0)  # Then by popularity
            ), reverse=True)
            
            result_tracks = tracks[:limit]
            print(f"Returning {len(result_tracks)} tracks")
            return result_tracks
            
        except Exception as e:
            print(f"Spotify Search API error: {e}")
            import traceback
            traceback.print_exc()
            return []


    # playlist method
    def create_playlist(self, name: str,  description: str = "", public: bool = False) -> Dict[str, Any]:
        user = self.me()
        user_id = user["id"]

        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=name,
            public=public,
            description=description
        )

        if playlist is None:
            raise RuntimeError("Failed to create playlist")

        return playlist
    
    def add_tracks_to_playlist(
        self,
        playlist_id: str,
        uris: List[str],
    ) -> None:
        self.sp.playlist_add_items(
            playlist_id=playlist_id,
            items=uris,
        )

    def audio_features(self, track_ids: List[str]) -> List[Dict[str, Any]]:
        feats = self.sp.audio_features(track_ids) or []
        return [f for f in feats if f is not None]


