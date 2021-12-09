import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import xarray as xr
from scipy import stats


def plot(data, x, y, type=None, **kwargs):
    """
    Function to plot the corr coeff plot
    --------------------------
    input 3 values data, x and y in this order
    and use this example -

    data = dataframe_name
    x = data['column_name']
    y = data['column_name']
    """

    r, p = stats.pearsonr(x,y)

    # checking value of p for reporting p in figure
    if p < 0.001:
        p_string = " and $p < .001$"
    else:
        p_string = f" and p = {np.round(p,3)}"

    # r = x - ((x.describe()[1]) *
    # (y - y.describe()[1])).describe()[1] / (y.describe()[2]*x.describe()[2])

    plt.scatter(
        x, y, label=f'r = {np.round(r, 3)}' + p_string, **kwargs)
    if type == 'compare':
        lineStartx = x.min() - 3
        lineEndx = x.max() + 3
        lineStarty = y.min() - 3
        lineEndy = y.max() + 3

        sns.regplot(x=x, y=y, data=data, color='k', scatter=False,
                    fit_reg=True, truncate=False, label='Linear Fit').set(xlabel=None, ylabel=None)
        # plt.plot([lineStartx, lineEndx], [
        # lineStarty, lineEndy], 'k-', color='k')
        # plt.plot([lineStartx, lineEndx], [lineStarty, 0.5773*lineEndy],
        # 'k--', color='k', alpha=0.5)
        # plt.plot([lineStartx, lineEndx], [lineStarty, 1.7321*lineEndy],
        # 'k--', color='k', alpha=0.5)
        plt.xlim(lineStartx, lineEndx)
        plt.ylim(lineStarty, lineEndy)
        plt.legend(frameon = True, loc=0, prop={'size': 10})

    if type == 'logistic':
        lineStartx = x.min()
        lineEndx = x.max()
        lineStarty = y.min()
        lineEndy = y.max()

        sns.regplot(x=x, y=y, data=data, color='k', scatter=False,
                    fit_reg=True, logx = True, truncate=False, label='Regression Fit').set(xlabel=None, ylabel=None)
        # plt.plot([lineStartx, lineEndx], [
        # lineStarty, lineEndy], 'k-', color='k')
        # plt.plot([lineStartx, lineEndx], [lineStarty, 0.5773*lineEndy],
        # 'k--', color='k', alpha=0.5)
        # plt.plot([lineStartx, lineEndx], [lineStarty, 1.7321*lineEndy],
        # 'k--', color='k', alpha=0.5)
        plt.xlim(lineStartx, lineEndx)
        plt.ylim(lineStarty, lineEndy)
        plt.legend(frameon = True, loc=0, prop={'size': 10})

    if type == None:
        if x.min() < y.min():
            lineStart = x.min()
        else:
            lineStart = y.min()

        if x.max() > y.max():
            lineEnd = x.max()
        else:
            lineEnd = y.max()

        sns.regplot(x=x, y=y, data=data, color='r', scatter=False,
                    fit_reg=True, truncate=False, label='Linear Fit').set(xlabel=None, ylabel=None)
        plt.plot([lineStart, lineEnd], [lineStart, lineEnd], 'k-', alpha = 0.7)
        # plt.plot([lineStart, lineEnd], [lineStart, 0.5773*lineEnd],
        #          'k--', color='k', alpha=0.5)
        # plt.plot([lineStart, lineEnd], [lineStart, 1.7321*lineEnd],
        #          'k--', color='k', alpha=0.5)
        plt.xlim(lineStart, lineEnd)
        plt.ylim(lineStart, lineEnd)
        plt.legend(frameon = True, loc=0, prop={'size': 12})

def plot_binning(data, x, y, bins, **kwargs):
    """
    Function to plot the corr coeff plot for the binned data
    --------------------------
    input 3 values dataset, x and y in this order
    and use this example -

    data = dataset_name
    x = data['column_name']
    y = data['column_name']
    """

    binned_x = data[x].groupby_bins(data[x], bins).mean()
    binned_y = data[y].groupby_bins(data[x], bins).mean()
    binned_yerr = data[y + '_stdev'].groupby_bins(data[x], bins).mean()

    slope, intercept, r, p, _ = stats.linregress(binned_x, binned_y)

    plt.scatter(data[x], data[y], **kwargs)

    if p < 0.001:
        plt.plot(binned_x, slope*binned_x + intercept, color = kwargs['color'], label = f'R = {np.round(r,3)}; p < 0.001')
    else:
        plt.plot(binned_x, slope*binned_x + intercept, color = kwargs['color'], label=f'R = {np.round(r,3)} and p = {np.round(p,3)}')
    (_, caps, _) = plt.errorbar(binned_x, binned_y, yerr=binned_yerr,
                            alpha=0.9, ecolor='k', fmt='^',
                            mfc='k', markersize=6, capsize=4, label='binned average')
    plt.legend(frameon=False, loc=0)
