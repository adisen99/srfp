import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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
        lineStartx = x.min()
        lineEndx = x.max()
        lineStarty = y.min()
        lineEndy = y.max()

        sns.regplot(x=x, y=y, data=data, color='k', scatter=False,
                    fit_reg=True, truncate=True, label='Linear Fit').set(xlabel=None, ylabel=None)
        # plt.plot([lineStartx, lineEndx], [
        # lineStarty, lineEndy], 'k-', color='k')
        # plt.plot([lineStartx, lineEndx], [lineStarty, 0.5773*lineEndy],
        # 'k--', color='k', alpha=0.5)
        # plt.plot([lineStartx, lineEndx], [lineStarty, 1.7321*lineEndy],
        # 'k--', color='k', alpha=0.5)
        plt.xlim(lineStartx, lineEndx)
        plt.ylim(lineStarty, lineEndy)
        plt.legend(frameon = True, loc=0, prop={'size': 12})

    if type == 'logistic':
        lineStartx = x.min()
        lineEndx = x.max()
        lineStarty = y.min()
        lineEndy = y.max()

        sns.regplot(x=x, y=y, data=data, color='k', scatter=False,
                    fit_reg=True, logx = True, truncate=True, label='Regression Fit').set(xlabel=None, ylabel=None)
        # plt.plot([lineStartx, lineEndx], [
        # lineStarty, lineEndy], 'k-', color='k')
        # plt.plot([lineStartx, lineEndx], [lineStarty, 0.5773*lineEndy],
        # 'k--', color='k', alpha=0.5)
        # plt.plot([lineStartx, lineEndx], [lineStarty, 1.7321*lineEndy],
        # 'k--', color='k', alpha=0.5)
        plt.xlim(lineStartx, lineEndx)
        plt.ylim(lineStarty, lineEndy)
        plt.legend(frameon = True, loc=0, prop={'size': 12})

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
                    fit_reg=True, truncate=True, label='Linear Fit').set(xlabel=None, ylabel=None)
        plt.plot([lineStart, lineEnd], [lineStart, lineEnd], 'k-', color='k', alpha = 0.7)
        # plt.plot([lineStart, lineEnd], [lineStart, 0.5773*lineEnd],
        #          'k--', color='k', alpha=0.5)
        # plt.plot([lineStart, lineEnd], [lineStart, 1.7321*lineEnd],
        #          'k--', color='k', alpha=0.5)
        plt.xlim(lineStart, lineEnd)
        plt.ylim(lineStart, lineEnd)
        plt.legend(frameon = True, loc=0, prop={'size': 12})
