import numpy as np

def clamp(value, minBound, maxBound):
    return np.clip(value, minBound, maxBound)