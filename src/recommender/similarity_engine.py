from typing import Dict, List

def explain_similarity(user_features: Dict[str, float], spotify_audio_feat: Dict) -> str:
    """
    Basic explanation comparing your audio to Spotify audio-features.
    We'll improve later.
    """
    parts = []
    tempo = user_features.get("tempo_bpm")
    if tempo is not None and spotify_audio_feat.get("tempo") is not None:
        parts.append(f"tempo match (you≈{tempo:.0f} BPM, rec≈{spotify_audio_feat['tempo']:.0f} BPM)")
    if spotify_audio_feat.get("energy") is not None:
        parts.append(f"energy≈{spotify_audio_feat['energy']:.2f}")
    if spotify_audio_feat.get("valence") is not None:
        parts.append(f"valence≈{spotify_audio_feat['valence']:.2f}")
    return " • ".join(parts) if parts else "Similar vibe based on Spotify audio features."
