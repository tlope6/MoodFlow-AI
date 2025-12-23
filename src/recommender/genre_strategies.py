# src/recommender/genre_strategies.py
from typing import Dict, List

# Define top artists for genres where Spotify's genre tags are unreliable
GENRE_SEED_ARTISTS = {
    "k-pop": [
        "BTS", "BLACKPINK", "Stray Kids", "NewJeans", "Jungkook",
        "Jimin", "TWICE", "SEVENTEEN", "Enhypen", "TXT"
    ],
    "j-pop": [
        "Yoasobi", "Official HIGE DANdism", "Ado", "King Gnu",
        "Eve", "Kenshi Yonezu", "LiSA", "Aimer"
    ],
    "anime": [
        "LiSA", "Aimer", "Yoasobi", "Kenshi Yonezu", "Eve",
        "Asian Kung-Fu Generation", "Unison Square Garden"
    ],
    "latin": [
        "Bad Bunny", "Karol G", "Peso Pluma", "Feid", "Rauw Alejandro",
        "Myke Towers", "Rosalía", "J Balvin"
    ],
    "reggaeton": [
        "Bad Bunny", "Karol G", "Daddy Yankee", "Ozuna", "Nicky Jam",
        "Maluma", "J Balvin", "Rauw Alejandro"
    ],
    "afrobeat": [
        "Burna Boy", "Wizkid", "Tems", "Rema", "Asake",
        "Ayra Starr", "Fireboy DML", "Omah Lay"
    ],
    "brazil": [
        "Anitta", "Ludmilla", "Pabllo Vittar", "Mc Don Juan",
        "Alok", "Vintage Culture"
    ]
}

# Genres that need artist-focused search (not reliable genre tags)
ARTIST_FOCUSED_GENRES = set(GENRE_SEED_ARTISTS.keys())

# Genres that work well with year filtering for freshness
TIME_SENSITIVE_GENRES = {
    "edm", "house", "techno", "dubstep", "trap", "hip-hop",
    "pop", "k-pop", "j-pop", "latin", "reggaeton", "afrobeat"
}

# Genres that benefit from mood/vibe keywords
MOOD_BASED_GENRES = {
    "chill": ["relaxing", "calm", "study"],
    "sad": ["melancholic", "emotional", "heartbreak"],
    "happy": ["upbeat", "feel good", "positive"],
    "party": ["dance", "club", "party"],
    "work-out": ["gym", "workout", "motivation", "energy"]
}


def get_search_strategy(genre: str) -> Dict:
    """
    Returns the optimal search strategy for a given genre
    """
    strategy = {
        "use_artist_search": genre in ARTIST_FOCUSED_GENRES,
        "seed_artists": GENRE_SEED_ARTISTS.get(genre, []),
        "use_year_filter": genre in TIME_SENSITIVE_GENRES,
        "mood_keywords": MOOD_BASED_GENRES.get(genre, []),
        "prioritize_related_artists": genre in ARTIST_FOCUSED_GENRES,
        "max_related_artists": 8 if genre in ARTIST_FOCUSED_GENRES else 5
    }
    return strategy