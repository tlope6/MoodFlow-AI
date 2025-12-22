import librosa
import numpy as np
from typing import IO, Tuple, Union

AudioInput = Union[str, IO[bytes]]

def load_audio(inp: AudioInput, sr: int = 22050, mono: bool = True) -> Tuple[np.ndarray, int]:
    """
    Load audio from a file path OR a file-like object (Streamlit upload).
    """
    y, sr = librosa.load(inp, sr=sr, mono=mono)
    return y, sr
