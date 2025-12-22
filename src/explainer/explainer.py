from typing import Dict, Optional

def explain_recommendation(mood: str, genre: str, user_features: Dict[str, float]) -> str:
    tempo = user_features.get("tempo_bpm", 0.0)
    bright = user_features.get("spectral_centroid_mean", 0.0)

    lines = []
    lines.append(f"I predicted **{genre}** based on your audio profile.")
    lines.append(f"Mood estimate: **{mood}**.")
    lines.append(f"Your track’s tempo is about **{tempo:.0f} BPM** and brightness about **{bright:.0f}**.")
    lines.append("I used those to pull Spotify artists, tracks, and playlists that match that vibe.")
    return "\n".join(lines)
