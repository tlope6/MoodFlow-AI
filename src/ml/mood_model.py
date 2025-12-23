def predict_mood(audio_feat: dict) -> str:

    energy = audio_feat.get("energy", 0.5)
    tempo = audio_feat.get("tempo_bpm", 120)
    spectral_centroid = audio_feat.get("spectral_centroid", 2000)
    
    # High energy + fast tempo = happy/energetic
    if energy > 0.7 and tempo > 120:
        return "happy"
    
    # High energy + slower tempo = energetic but intense
    if energy > 0.7 and tempo <= 120:
        return "energetic"
    
    # Low energy + slow tempo = sad/melancholic
    if energy < 0.4 and tempo < 100:
        return "sad"
    
    # Low energy + medium tempo = calm/relaxed
    if energy < 0.4:
        return "calm"
    
    # Everything else
    return "neutral"