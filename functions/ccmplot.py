import skccm as ccm
import skccm.data as data
import matplotlib.pyplot as plt
import numpy as np
from skccm.utilities import train_test_split

def plot(x1, x2, names):
    """
    Plotting the convergent cross mapping between two variables,
    ----
    inputs : x1 (PM concentration); x2 (Meteorological parameter)
    output: Plots of xmap between the PM and Meteorological parameters
    """
    lag = 1
    embed = 3
    e1 = ccm.Embed(x1)
    e2 = ccm.Embed(x2)
    X1 = e1.embed_vectors_1d(lag, embed)
    X2 = e2.embed_vectors_1d(lag,embed)

    #split the embedded time series
    x1tr, x1te, x2tr, x2te = train_test_split(X1,X2, percent=.75)

    CCM = ccm.CCM() #initiate the class

    #library lengths to test
    len_tr = len(x1tr)
    lib_lens = np.arange(10, len_tr, len_tr/20, dtype='int')

    #test causation
    CCM.fit(x1tr,x2tr)
    x1p, x2p = CCM.predict(x1te, x2te,lib_lengths=lib_lens)

    sc1,sc2 = CCM.score()

    plt.plot(lib_lens, sc1, label = f"{names[0]} xmap {names[1]}")
    plt.plot(lib_lens, sc2, label = f"{names[1]} xmap {names[0]}")
    plt.legend(loc = 0, frameon = False)
