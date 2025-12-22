from typing import Dict

def predict_genre(features: Dict[str, float]) -> str:
    
    # Baseline heuristic genre guess.
    # Spotify 'seed_genres' must be valid Spotify genres; we'll map later.
    
    tempo = features.get("tempo_bpm", 0.0)
    centroid = features.get("spectral_centroid_mean", 0.0)

    if tempo >= 135:
        return "edm"
    if centroid >= 2400 and tempo >= 110:
        return "rock"
    if tempo <= 80:
        return "ambient"
    return "pop"
