from typing import Dict

def predict_mood(features: Dict[str, float]) -> str:
    
    # Baseline heuristic mood classifier.
    # Upgrade later to ML model or Spotify audio-features mapping.
    
    tempo = features.get("tempo_bpm", 0.0)
    centroid = features.get("spectral_centroid_mean", 0.0)

    if tempo >= 130 and centroid >= 2300:
        return "energetic"
    if tempo <= 85 and centroid <= 1800:
        return "calm"
    if 90 <= tempo <= 125 and centroid >= 2000:
        return "happy"
    return "neutral"
