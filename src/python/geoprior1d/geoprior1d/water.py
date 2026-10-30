import numpy as np

def prior_water_reals(info):
  
    # min/max are read as 1-element arrays; use plain floats so the sample is a scalar
    w_min = float(np.ravel(info['Water Level']['min'])[0])
    w_max = float(np.ravel(info['Water Level']['max'])[0])
    o = np.random.rand() * (w_max - w_min) + w_min
    return o
