def predict_mood(audio_feat: dict) -> str:
    energy = audio_feat.get("energy", 0)
    valence = audio_feat.get("valence", 0)
    dance = audio_feat.get("danceability", 0)

    if energy > 0.75 and valence > 0.6:
        return "happy"
    if energy > 0.75 and valence < 0.4:
        return "energetic"
    if energy < 0.35 and valence < 0.4:
        return "sad"
    if energy < 0.35:
        return "calm"
    return "neutral"
