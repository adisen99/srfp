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

    plt.plot(times, dfmod[mod]['mean'], color='tab:red', label='model')

    if mod_stdev is not None:
        (_, caps, _) = plt.errorbar(times, dfmod[mod]['mean'], yerr=dfmod[mod_stdev]['mean'],
                                    alpha=0.3, ecolor='tab:red', fmt='o', mfc='tab:red', markersize=8,
                                    capsize=10, label='stdev')

        for cap in caps:
            cap.set_markeredgewidth(1)

    plt.plot(times, dfobs[obs]['mean'], color='tab:blue', label='observed')

    if obs_stdev is not None:
        (_, caps, _) = plt.errorbar(times, dfobs[obs]['mean'], yerr=dfobs[obs_stdev]['mean'],
                                    alpha=0.3, ecolor='tab:blue', fmt='o', mfc='tab:blue', markersize=8,
                                    capsize=10, label='stdev')

        for cap in caps:
            cap.set_markeredgewidth(1)

    plt.legend(ncol=2, frameon=False, loc='right', bbox_to_anchor=(1.02, 1.13), prop={'size': 12})
    plt.xticks(np.arange(0, 24, step=1))
