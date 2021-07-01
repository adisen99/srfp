"""
python module to calculate the aqi and quality
"""

import pandas as pd
import numpy as np

# Defining functions for finding CPCB AQI using pm2.5 and pm10 running mean data


def mod_aqi_pm2(c):
    if c['mod_pm2'] > 0 and c['mod_pm2'] <= 30:
        return (1.66*(c['mod_pm2'] - 0)) + 0
    elif c['mod_pm2'] > 30 and c['mod_pm2'] <= 60:
        return (1.66*(c['mod_pm2'] - 30)) + 50
    elif c['mod_pm2'] > 60 and c['mod_pm2'] <= 90:
        return (3.33*(c['mod_pm2'] - 60)) + 100
    elif c['mod_pm2'] > 90 and c['mod_pm2'] <= 120:
        return (3.33*(c['mod_pm2'] - 90)) + 200
    elif c['mod_pm2'] > 120 and c['mod_pm2'] <= 250:
        return (0.769*(c['mod_pm2'] - 120)) + 300
    elif c['mod_pm2'] > 250:
        return (0.769*(c['mod_pm2'] - 250)) + 400
    else:
        return np.nan


def mod_aqi_pm10(c):
    if c['mod_pm10'] > 0 and c['mod_pm10'] <= 50:
        return ((c['mod_pm10'] - 0)) + 0
    elif c['mod_pm10'] > 50 and c['mod_pm10'] <= 100:
        return ((c['mod_pm10'] - 50)) + 50
    elif c['mod_pm10'] > 100 and c['mod_pm10'] <= 250:
        return (0.66*(c['mod_pm10'] - 100)) + 100
    elif c['mod_pm10'] > 250 and c['mod_pm10'] <= 350:
        return ((c['mod_pm10'] - 250)) + 200
    elif c['mod_pm10'] > 350 and c['mod_pm10'] <= 430:
        return (1.25*(c['mod_pm10'] - 350)) + 300
    elif c['mod_pm10'] > 430:
        return (1.25*(c['mod_pm10'] - 430)) + 400
    else:
        return np.nan


def obs_aqi_pm2(c):
    if c['obs_pm2'] > 0 and c['obs_pm2'] <= 30:
        return (1.66*(c['obs_pm2'] - 0)) + 0
    elif c['obs_pm2'] > 30 and c['obs_pm2'] <= 60:
        return (1.66*(c['obs_pm2'] - 30)) + 50
    elif c['obs_pm2'] > 60 and c['obs_pm2'] <= 90:
        return (3.33*(c['obs_pm2'] - 60)) + 100
    elif c['obs_pm2'] > 90 and c['obs_pm2'] <= 120:
        return (3.33*(c['obs_pm2'] - 90)) + 200
    elif c['obs_pm2'] > 120 and c['obs_pm2'] <= 250:
        return (0.769*(c['obs_pm2'] - 120)) + 300
    elif c['obs_pm2'] > 250:
        return (0.769*(c['obs_pm2'] - 250)) + 400
    else:
        return np.nan


def obs_aqi_pm10(c):
    if c['obs_pm10'] > 0 and c['obs_pm10'] <= 50:
        return ((c['obs_pm10'] - 0)) + 0
    elif c['obs_pm10'] > 50 and c['obs_pm10'] <= 100:
        return ((c['obs_pm10'] - 50)) + 50
    elif c['obs_pm10'] > 100 and c['obs_pm10'] <= 250:
        return (0.66*(c['obs_pm10'] - 100)) + 100
    elif c['obs_pm10'] > 250 and c['obs_pm10'] <= 350:
        return ((c['obs_pm10'] - 250)) + 200
    elif c['obs_pm10'] > 350 and c['obs_pm10'] <= 430:
        return (1.25*(c['obs_pm10'] - 350)) + 300
    elif c['obs_pm10'] > 430:
        return (1.25*(c['obs_pm10'] - 430)) + 400
    else:
        return np.nan


def get_aqi(dfmod, dfobs):

    # Taking the rolling mean
    dfmod['mod_pm2'] = dfmod['mod_PM2.5'].rolling(24).mean()
    dfmod['mod_pm2_stdev'] = dfmod['mod_PM2.5_stdev'].rolling(24).mean()
    dfmod['mod_pm10'] = dfmod['mod_PM10'].rolling(24).mean()
    dfmod['mod_pm10_stdev'] = dfmod['mod_PM10_stdev'].rolling(24).mean()

    dfobs['obs_pm2'] = dfobs['obs_PM2.5'].rolling(24).mean()
    dfobs['obs_pm2_stdev'] = dfobs['obs_PM2.5_stdev'].rolling(24).mean()
    dfobs['obs_pm10'] = dfobs['obs_PM10'].rolling(24).mean()
    dfobs['obs_pm10_stdev'] = dfobs['obs_PM10_stdev'].rolling(24).mean()

    # Dropping the unwanted values
    dfmod = dfmod.drop(['mod_PM2.5_stdev', 'mod_PM10_stdev',
                        'datetime', 'month', 'time'], axis=1)

    dfobs = dfobs.drop(['obs_PM2.5_stdev', 'obs_PM10_stdev',
                        'datetime', 'month', 'time'], axis=1)

    # Getting the aqi columns
    dfmod['mod_aqi_pm2'] = dfmod.apply(mod_aqi_pm2, axis=1)
    dfmod['mod_aqi_pm10'] = dfmod.apply(mod_aqi_pm10, axis=1)

    dfobs['obs_aqi_pm2'] = dfobs.apply(obs_aqi_pm2, axis=1)
    dfobs['obs_aqi_pm10'] = dfobs.apply(obs_aqi_pm10, axis=1)

    # Get the quality
    quality_mod_pm25 = []

    # 0 -> good
    # 1 -> satisfactory
    # 2 -> moderately polluted
    # 3 -> poor
    # 4 -> very poor
    # 5 -> severe

    for aqipm25mod in dfmod['mod_aqi_pm2']:

        if aqipm25mod >= 0 and aqipm25mod <= 50:
            quality_mod_pm25.append(0)
        elif aqipm25mod > 50 and aqipm25mod <= 100:
            quality_mod_pm25.append(1)
        elif aqipm25mod > 100 and aqipm25mod <= 200:
            quality_mod_pm25.append(2)
        elif aqipm25mod > 200 and aqipm25mod <= 300:
            quality_mod_pm25.append(3)
        elif aqipm25mod > 300 and aqipm25mod <= 400:
            quality_mod_pm25.append(4)
    #     elif aqipm25mod > 400 and aqipm25mod <= 500:
    #         quality_mod_pm25.append(5)
        else:
            quality_mod_pm25.append(5)

    quality_mod_pm10 = []

    for aqipm10mod in dfmod['mod_aqi_pm10']:

        if aqipm10mod >= 0 and aqipm10mod <= 50:
            quality_mod_pm10.append(0)
        elif aqipm10mod > 50 and aqipm10mod <= 100:
            quality_mod_pm10.append(1)
        elif aqipm10mod > 100 and aqipm10mod <= 200:
            quality_mod_pm10.append(2)
        elif aqipm10mod > 200 and aqipm10mod <= 300:
            quality_mod_pm10.append(3)
        elif aqipm10mod > 300 and aqipm10mod <= 400:
            quality_mod_pm10.append(4)
    #     elif aqipm10mod > 400 and aqipm10mod <= 500:
    #         quality_mod_pm10.append(5)
        else:
            quality_mod_pm10.append(5)

    quality_obs_pm25 = []

    for aqipm25obs in dfobs['obs_aqi_pm2']:

        if aqipm25obs >= 0 and aqipm25obs <= 50:
            quality_obs_pm25.append(0)
        elif aqipm25obs > 50 and aqipm25obs <= 100:
            quality_obs_pm25.append(1)
        elif aqipm25obs > 100 and aqipm25obs <= 200:
            quality_obs_pm25.append(2)
        elif aqipm25obs > 200 and aqipm25obs <= 300:
            quality_obs_pm25.append(3)
        elif aqipm25obs > 300 and aqipm25obs <= 400:
            quality_obs_pm25.append(4)
    #     elif aqipm25obs > 400 and aqipm25obs <= 500:
    #         quality_obs_pm25.append(5)
        else:
            quality_obs_pm25.append(5)

    quality_obs_pm10 = []

    for aqipm10obs in dfobs['obs_aqi_pm10']:

        if aqipm10obs >= 0 and aqipm10obs <= 50:
            quality_obs_pm10.append(0)
        elif aqipm10obs > 50 and aqipm10obs <= 100:
            quality_obs_pm10.append(1)
        elif aqipm10obs > 100 and aqipm10obs <= 200:
            quality_obs_pm10.append(2)
        elif aqipm10obs > 200 and aqipm10obs <= 300:
            quality_obs_pm10.append(3)
        elif aqipm10obs > 300 and aqipm10obs <= 400:
            quality_obs_pm10.append(4)
    #     elif aqipm10obs > 400 and aqipm10obs <= 500:
    #         quality_obs_pm10.append(5)
        else:
            quality_obs_pm10.append(5)

    dfmod['quality_mod_pm25'] = quality_mod_pm25
    dfmod['quality_mod_pm10'] = quality_mod_pm10

    dfobs['quality_obs_pm25'] = quality_obs_pm25
    dfobs['quality_obs_pm10'] = quality_obs_pm10

    dfmod = dfmod.dropna()
    dfobs = dfobs.dropna()

    df = pd.concat([dfmod, dfobs], axis=1)

    return df
