import librosa
import numpy as np
from typing import Any, Tuple, Union

AudioInput = Union[str, Any]

def load_audio(
    inp: AudioInput,
    sr: int = 22050,
    mono: bool = True
) -> Tuple[np.ndarray, int]:
    """
    Load audio from a file path OR a Streamlit UploadedFile.
    """
    y, sample_rate = librosa.load(inp, sr=sr, mono=mono)
    return y, int(sample_rate)
