"""
Python module to calculate the Statistical performance
"""

import numpy as np
import pandas as pd
from scipy import stats

# Single function to obtain the statistical performance measures


def get_stat_performance(df, type=None):

    if type == 'aqi':

        request = int(input("Raw data[1] or Running mean data [2]: "))

        if request == 1:
            mod_pm2 = 'mod_PM2.5'
            obs_pm2 = 'obs_PM2.5'
            mod_pm10 = 'mod_PM10'
            obs_pm10 = 'obs_PM10'
        elif request == 2:
            mod_pm2 = 'mod_pm2'
            obs_pm2 = 'obs_pm2'
            mod_pm10 = 'mod_pm10'
            obs_pm10 = 'obs_pm10'
        else:
            print("Enter either 1 or 2")

        # mean bias

        mb_pm25 = (df[mod_pm2] - df[obs_pm2]).describe()[1]
        mb_pm10 = (df[mod_pm10] - df[obs_pm10]).describe()[1]
        mb_aqi25 = (df['mod_aqi_pm2'] - df['obs_aqi_pm2']).describe()[1]
        mb_aqi10 = (df['mod_aqi_pm10'] - df['obs_aqi_pm10']).describe()[1]

        print("Mean bias :")
        print("mean bias pm2.5 = ", mb_pm25)
        print("mean bias pm10 = ", mb_pm10)
        print("mean bias aqi_pm2.5 = ", mb_aqi25)
        print("mean bias aqi_pm10 = ", mb_aqi10, "\n")

        # fractional bias

        fb_pm25 = 2 * ((df[mod_pm2].describe()[1] - df[obs_pm2].describe()[1]) /
                       (df[mod_pm2].describe()[1] + df[obs_pm2].describe()[1]))
        fb_pm10 = 2 * ((df[mod_pm10].describe()[1] - df[obs_pm10].describe()[1]) /
                       (df[mod_pm10].describe()[1] + df[obs_pm10].describe()[1]))
        fb_aqi25 = 2 * ((df['mod_aqi_pm2'].describe()[1] - df['obs_aqi_pm2'].describe()[1]) /
                        (df['mod_aqi_pm2'].describe()[1] + df['obs_aqi_pm2'].describe()[1]))
        fb_aqi10 = 2 * ((df['mod_aqi_pm10'].describe()[1] - df['obs_aqi_pm10'].describe()[1]) /
                        (df['mod_aqi_pm10'].describe()[1] + df['obs_aqi_pm10'].describe()[1]))

        print("fractional bias is :")
        print("fractional bias pm2.5 = ", fb_pm25)
        print("fractional bias pm10 = ", fb_pm10)
        print("fractional bias aqi_pm2.5 = ", fb_aqi25)
        print("fractional bias aqi_pm10 = ", fb_aqi10, "\n")

        # Pearson's Corr Coeff

        # r_pm25 = ((df[obs_pm2] - df[obs_pm2].describe()[1]) *
        #           (df[mod_pm2] - df[mod_pm2].describe()[1])).describe()[1] / (df[mod_pm2].describe()[2] *
        #                                                                       df[obs_pm2].describe()[2])

        # r_pm10 = ((df[obs_pm10] - df[obs_pm10].describe()[1]) *
        #           (df[mod_pm10] - df[mod_pm10].describe()[1])).describe()[1] / (df[mod_pm10].describe()[2] *
        #                                                                         df[obs_pm10].describe()[2])

        # r_aqi25 = ((df['obs_aqi_pm2'] - df['obs_aqi_pm2'].describe()[1]) *
        #            (df['mod_aqi_pm2'] - df['mod_aqi_pm2'].describe()[1])).describe()[1] / (df['mod_aqi_pm2'].describe()[2] * df['obs_aqi_pm2'].describe()[2])

        # r_aqi10 = ((df['obs_aqi_pm10'] - df['obs_aqi_pm10'].describe()[1]) *
        #            (df['mod_aqi_pm10'] - df['mod_aqi_pm10'].describe()[1])).describe()[1] / (df['mod_aqi_pm10'].describe()[2] * df['obs_aqi_pm10'].describe()[2])

        r_pm25, p_pm25 = stats.pearsonr(df[obs_pm2], df[mod_pm2])

        r_pm10, p_pm10 = stats.pearsonr(df[obs_pm10], df[mod_pm10])

        r_aqi25, p_aqi25 = stats.pearsonr(df['obs_aqi_pm2'], df['mod_aqi_pm2'])

        r_aqi10, p_aqi10 = stats.pearsonr(df['obs_aqi_pm10'], df['mod_aqi_pm10'])

        print("Correlation coefficient is :")
        print("corr coeff pm2.5 = ", r_pm25, " and p-value is = ", p_pm25)
        print("corr coeff pm10 = ", r_pm10, " and p-value is = ", p_pm10)
        print("corr coeff aqi_pm2.5 = ", r_aqi25, " and p-value is = ", p_aqi25)
        print("corr coeff aqi_pm10 = ", r_aqi10, "\n", " and p-value is = ", p_aqi10)

        # RMSE

        rmse_pm25 = np.sqrt(((df[mod_pm2] - df[obs_pm2])
                            * (df[mod_pm2] - df[obs_pm2])).describe()[1])
        rmse_pm10 = np.sqrt(((df[mod_pm10] - df[obs_pm10])
                            * (df[mod_pm10] - df[obs_pm10])).describe()[1])
        rmse_aqi25 = np.sqrt(((df['mod_aqi_pm2'] - df['obs_aqi_pm2']) *
                              (df['mod_aqi_pm2'] - df['obs_aqi_pm2'])).describe()[1])
        rmse_aqi10 = np.sqrt(((df['mod_aqi_pm10'] - df['obs_aqi_pm10']) *
                              (df['mod_aqi_pm10'] - df['obs_aqi_pm10'])).describe()[1])

        print("RMSE is :")
        print("RMSE pm2.5 = ", rmse_pm25)
        print("RMSE pm10 = ", rmse_pm10)
        print("RMSE aqi_pm2.5 = ", rmse_aqi25)
        print("RMSE aqi_pm10 = ", rmse_aqi10, "\n")
        
        # NMSE

        nmse_pm25 = (((df[mod_pm2] - df[obs_pm2]) * (df[mod_pm2] - df[obs_pm2])).describe()[1]) \
                / (df[obs_pm2].describe()[1] * df[mod_pm2].describe()[1])

        nmse_pm10 = (((df[mod_pm10] - df[obs_pm10]) * (df[mod_pm10] - df[obs_pm10])).describe()[1]) \
                / (df[obs_pm10].describe()[1] * df[mod_pm10].describe()[1])

        nmse_aqi25 = (((df['mod_aqi_pm2'] - df['obs_aqi_pm2']) * (df['mod_aqi_pm2'] - df['obs_aqi_pm2'])).describe()[1]) \
                / (df['obs_aqi_pm2'].describe()[1] * df['mod_aqi_pm2'].describe()[1])
        nmse_aqi10 = (((df['mod_aqi_pm10'] - df['obs_aqi_pm10']) * (df['mod_aqi_pm10'] - df['obs_aqi_pm10'])).describe()[1]) \
                / (df['obs_aqi_pm10'].describe()[1] * df['mod_aqi_pm10'].describe()[1])

        print("NMSE is :")
        print("NMSE pm2.5 = ", nmse_pm25)
        print("NMSE pm10 = ", nmse_pm10)
        print("NMSE aqi_pm2.5 = ", nmse_aqi25)
        print("NMSE aqi_pm10 = ", nmse_aqi10, "\n")

    if type == None:

        mod = input("Enter the column for model value: ")
        obs = input("Enter the column for observation value: ")

        # mean bias

        mb = (df[mod] - df[obs]).describe()[1]

        print("Mean bias :")
        print("mean bias", mb)

        # fractional bias

        fb = 2 * ((df[mod].describe()[1] - df[obs].describe()[1]) /
                  (df[mod].describe()[1] + df[obs].describe()[1]))

        print("fractional bias is :")
        print("fractional bias = ", fb)

        # Pearson's Corr Coeff

        # r = ((df[obs] - df[obs].describe()[1]) *
        #      (df[mod] - df[mod].describe()[1])).describe()[1] / \
        #     (df[mod].describe()[2] * df[obs].describe()[2])

        r, p = stats.pearsonr(df[obs], df[mod])

        print("Correlation coefficient is :")
        print("corr coeff = ", r, " and p-value is = ", p)

        # RMSE

        rmse = np.sqrt(((df[mod] - df[obs])*(df[mod] - df[obs])).describe()[1])

        print("RMSE is :")
        print("RMSE ", rmse)

        # NMSE

        nmse = (((df[mod] - df[obs])*(df[mod] - df[obs])).describe()[1]) / (df[obs].describe()[1] * df[mod].describe()[1])

        print("NMSE is :")
        print("NMSE ", nmse)
