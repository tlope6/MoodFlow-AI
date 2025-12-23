# src/ml/genre_model.py
from typing import Dict


def predict_genre(features: Dict) -> str:
    """
    Predict a high-level music genre from extracted audio features.

    This is a semantic prediction (ML-facing),
    not constrained to Spotify seed genres.
    """

    energy = features.get("energy", 0.5)
    tempo = features.get("tempo_bpm", 120)
    spectral_centroid = features.get("spectral_centroid", 2000)

    # Simple rule-based baseline (replace with ML later)
    if energy > 0.8 and tempo > 130:
        return "edm"
    elif energy > 0.7:
        return "rock"
    elif spectral_centroid < 1500 and tempo < 100:
        return "lofi"
    elif energy < 0.4:
        return "ambient"
    elif tempo < 90:
        return "jazz"
    else:
        return "pop"
