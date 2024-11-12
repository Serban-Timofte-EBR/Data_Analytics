import numpy as np
import pandas as pd


def procente(t):
    # print(t)
    assert isinstance(t, pd.Series)
    return t * 100 / t.sum()


def disim(t, coloane):
    x = t[coloane].values
    tx = np.sum(x, axis=0)
    tx[tx == 0] = 1
    sx = np.sum(x, axis=1)
    r = (sx - x.T).T
    tr = np.sum(r, axis=0)
    tr[tr == 0] = 1
    d = 0.5 * np.sum(np.abs(x / tx - r / tr),axis=0)
    return pd.Series(d, coloane)
