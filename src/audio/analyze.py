from typing import Dict, IO, Union
from src.audio.loader import load_audio
from src.audio.features import extract_features

AudioInput = Union[str, IO[bytes]]

def analyze_audio(inp: AudioInput) -> Dict[str, float]:
    #one call audio analysis for the app
    y, sr = load_audio(inp)
    return extract_features(y, sr)
