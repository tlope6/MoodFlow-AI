
from typing import Dict

def explain_recommendation(mood: str, genre: str, targets: Dict, features: Dict) -> str:
    parts = [f"**Mood:** {mood}", f"**Genre seed:** {genre}"]

    if "target_energy" in targets and "energy" in features:
        parts.append(f"Energy {features['energy']:.2f} (target {targets['target_energy']:.2f})")
    if "target_valence" in targets and "valence" in features:
        parts.append(f"Valence {features['valence']:.2f} (target {targets['target_valence']:.2f})")
    if "target_danceability" in targets and "danceability" in features:
        parts.append(f"Danceability {features['danceability']:.2f} (target {targets['target_danceability']:.2f})")

    return " • ".join(parts)
