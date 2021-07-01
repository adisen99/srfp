import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Function to plot diurnal variaiton for given dataframe as input

# Plot mean diurnal variation PM2.5


def plot(dfmod, dfobs, mod, obs, mod_stdev=None, obs_stdev=None):
    """
    Python function to plot the diurnal variation for
    hourly data in model and observation data frames
    ------------------------------------------------

    Example input:
        dplot.plot(dfmod, mod, obs, mod_stdev=str, obs_stdev=str)

        Here mod_stdev and obs_stdev are optional inputs
    """

    dfmod['time'] = dfmod.index.time
    dfobs['time'] = dfobs.index.time

    dfmod = dfmod.groupby('time').describe().unstack()
    dfobs = dfobs.groupby('time').describe().unstack()

    times = [x for x in range(0, 24)]

    plt.plot(times, dfmod[mod]['mean'], color='red', label='model')

    if mod_stdev is not None:
        (_, caps, _) = plt.errorbar(times, dfmod[mod]['mean'], yerr=dfmod[mod_stdev]['mean'],
                                    alpha=0.3, ecolor='red', fmt='o', mfc='red', markersize=8,
                                    capsize=10, label='stdev')

        for cap in caps:
            cap.set_markeredgewidth(1)

    plt.plot(times, dfobs[obs]['mean'], color='blue', label='observed')

    if obs_stdev is not None:
        (_, caps, _) = plt.errorbar(times, dfobs[obs]['mean'], yerr=dfobs[obs_stdev]['mean'],
                                    alpha=0.3, ecolor='blue', fmt='o', mfc='blue', markersize=8,
                                    capsize=10, label='stdev')

        for cap in caps:
            cap.set_markeredgewidth(1)

    plt.legend(loc=1, prop={'size': 12})
    plt.xticks(np.arange(0, 24, step=1))
