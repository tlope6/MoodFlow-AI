import librosa
import numpy as np
from typing import Dict

def extract_features(y: np.ndarray, sr: int) -> Dict[str, float]:
   
    feats: Dict[str, float] = {}

    # tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    feats["tempo_bpm"] = float(tempo)

    # brightness
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    feats["spectral_centroid_mean"] = float(np.mean(centroid))

    # noisiness / percussiveness proxy
    zcr = librosa.feature.zero_crossing_rate(y)
    feats["zcr_mean"] = float(np.mean(zcr))

    # mfcc summary
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    feats["mfcc_mean"] = float(np.mean(mfcc))
    feats["mfcc_std"] = float(np.std(mfcc))

    return feats
