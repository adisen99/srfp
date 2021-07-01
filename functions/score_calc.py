"""
Python module to calculate the score for critical,
very unhealthy and unhealthy air quality
"""

import numpy as np
import pandas as pd

# SCore calc for Critical Conditions (severe conditions only)


def get_critical_score(data):

    temp = data.copy(deep=True)

    conditions1 = [
        (temp['quality_mod_pm25'] == 5) & (temp['quality_obs_pm25'] == 5),
        (temp['quality_mod_pm25'] == 5) & (temp['quality_obs_pm25'] != 5),
        (temp['quality_mod_pm25'] != 5) & (temp['quality_obs_pm25'] == 5),
        (temp['quality_mod_pm25'] != 5) & (temp['quality_obs_pm25'] != 5)]

    choices1 = ['a', 'b', 'c', 'd']

    conditions2 = [
        (temp['quality_mod_pm10'] == 5) & (temp['quality_obs_pm10'] == 5),
        (temp['quality_mod_pm10'] == 5) & (temp['quality_obs_pm10'] != 5),
        (temp['quality_mod_pm10'] != 5) & (temp['quality_obs_pm10'] == 5),
        (temp['quality_mod_pm10'] != 5) & (temp['quality_obs_pm10'] != 5)]

    choices2 = ['a', 'b', 'c', 'd']

    temp['category_pm25'] = np.select(conditions1, choices1, default=np.nan)
    temp['category_pm10'] = np.select(conditions2, choices2, default=np.nan)

    test1 = temp.groupby('category_pm25')
    test2 = temp.groupby('category_pm10')

    # Need to write a program to give appropriate values to a,b,c and d
    key25 = []
    key10 = []

    for i in range(0, len(list(test1))):
        key25.append(list(test1)[i][0])

    for i in range(0, len(list(test2))):
        key10.append(list(test2)[i][0])

    val25 = []
    val10 = []

    for i in range(0, len(key25)):
        val25.append(list(test1)[i][1].shape[0])

    for i in range(0, len(key10)):
        val10.append(list(test2)[i][1].shape[0])

    res25 = dict(zip(key25, val25))
    res10 = dict(zip(key10, val10))

    expected = ['a', 'b', 'c', 'd']

    for j in expected:
        if j not in res25.keys():
            new25 = {j: 0}
            res25.update(new25)
        else:
            pass

    for j in expected:
        if j not in res10.keys():
            new10 = {j: 0}
            res10.update(new10)
        else:
            pass

    print("Key25 is : ", key25)
    print("The list25 from algorithm is : ", res25.keys())
    print("val25 is : ", res25.values())
    print("Key10 is : ", key10)
    print("The list10 from algorithm is : ", res10.keys())
    print("Val10 is : ", res10.values())

    a = res25['a']
    b = res25['b']
    c = res25['c']
    d = res25['d']

    A = ((a + d)/(a+b+c+d)) * 100  # Accuracy of events
    if a != 0 or b != 0:
        FAR = ((b)/(a+b)) * 100  # False event forecase
    if a != 0 or c != 0:
        POD = ((a)/(a+c)) * 100  # Expected events
    try:
        CSI = ((a)/(a+b+c)) * 100  # Events and event forecasts that were hits
        pointer1 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer1 = 1
    if a != 0 or c != 0:
        FOM = ((c)/(a+c))*100  # Surprise events
    if a != 0 or b != 0:
        FOH = ((a)/(a+b))*100  # Correct event forecasts
    if b != 0 or d != 0:
        PON = ((d)/(b+d))*100  # Expected non events
        POFD = ((b)/(b+d))*100  # Unexpected non events
    if c != 0 or d != 0:
        DFR = ((c)/(c+d))*100  # False non-event forecasts
        FOCN = ((d)/(c+d))*100  # Correct non-event forecasts
    try:
        # True skill statistic (Expected events  - unexpected non-events)
        TSS = ((a)/(a+c)) - ((b)/(b+d))
        Heidke = (((a+c)*(d-b))+((a-c)*(d+b)))/(((a+c)*(c+d))+((a+b)*(b+d)))
        pointer2 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer2 = 1

    print("Performance metrics or Skill score for Critical PM2.5 are:\n")

    print("A = ", A)
    if a != 0 or b != 0:
        print("FAR = ", FAR)
    if a != 0 or c != 0:
        print("POD = ", POD)
    if pointer1 == 0:
        print("CSI = ", CSI)
    if a != 0 or c != 0:
        print("FOM = ", FOM)
    if a != 0 or b != 0:
        print("FOH = ", FOH)
    if b != 0 or d != 0:
        print("PON = ", PON)
        print("POFD = ", POFD)
    if c != 0 or d != 0:
        print("DFR = ", DFR)
        print("FOCN = ", FOCN)
    if pointer2 == 0:
        print("TSS = ", TSS)
        print("Heidke = ", Heidke, "\n")

    a = res10['a']
    b = res10['b']
    c = res10['c']
    d = res10['d']

    A = ((a + d)/(a+b+c+d)) * 100  # Accuracy of events
    if a != 0 or b != 0:
        FAR = ((b)/(a+b)) * 100  # False event forecase
    if a != 0 or c != 0:
        POD = ((a)/(a+c)) * 100  # Expected events
    try:
        CSI = ((a)/(a+b+c)) * 100  # Events and event forecasts that were hits
        pointer1 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer1 = 1
    if a != 0 or c != 0:
        FOM = ((c)/(a+c))*100  # Surprise events
    if a != 0 or b != 0:
        FOH = ((a)/(a+b))*100  # Correct event forecasts
    if b != 0 or d != 0:
        PON = ((d)/(b+d))*100  # Expected non events
        POFD = ((b)/(b+d))*100  # Unexpected non events
    if c != 0 or d != 0:
        DFR = ((c)/(c+d))*100  # False non-event forecasts
        FOCN = ((d)/(c+d))*100  # Correct non-event forecasts
    try:
        # True skill statistic (Expected events  - unexpected non-events)
        TSS = ((a)/(a+c)) - ((b)/(b+d))
        Heidke = (((a+c)*(d-b))+((a-c)*(d+b)))/(((a+c)*(c+d))+((a+b)*(b+d)))
        pointer2 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer2 = 1

    print("Performance metrics or Skill score for Critical PM10 are:\n")

    print("A = ", A)
    if a != 0 or b != 0:
        print("FAR = ", FAR)
    if a != 0 or c != 0:
        print("POD = ", POD)
    if pointer1 == 0:
        print("CSI = ", CSI)
    if a != 0 or c != 0:
        print("FOM = ", FOM)
    if a != 0 or b != 0:
        print("FOH = ", FOH)
    if b != 0 or d != 0:
        print("PON = ", PON)
        print("POFD = ", POFD)
    if c != 0 or d != 0:
        print("DFR = ", DFR)
        print("FOCN = ", FOCN)
    if pointer2 == 0:
        print("TSS = ", TSS)
        print("Heidke = ", Heidke, "\n")


# SCore calc for Very Unhealthy Conditions (very poor, severe conditions only)

def get_veryunhealthy_score(data):

    temp = data.copy(deep=True)

    conditions1 = [
        (temp['quality_mod_pm25'] >= 4) & (temp['quality_obs_pm25'] >= 4),
        (temp['quality_mod_pm25'] >= 4) & (temp['quality_obs_pm25'] < 4),
        (temp['quality_mod_pm25'] < 4) & (temp['quality_obs_pm25'] >= 4),
        (temp['quality_mod_pm25'] < 4) & (temp['quality_obs_pm25'] < 4)]

    choices1 = ['a', 'b', 'c', 'd']

    conditions2 = [
        (temp['quality_mod_pm10'] >= 4) & (temp['quality_obs_pm10'] >= 4),
        (temp['quality_mod_pm10'] >= 4) & (temp['quality_obs_pm10'] < 4),
        (temp['quality_mod_pm10'] < 4) & (temp['quality_obs_pm10'] >= 4),
        (temp['quality_mod_pm10'] < 4) & (temp['quality_obs_pm10'] < 4)]

    choices2 = ['a', 'b', 'c', 'd']

    temp['category_pm25'] = np.select(conditions1, choices1, default=np.nan)
    temp['category_pm10'] = np.select(conditions2, choices2, default=np.nan)

    test1 = temp.groupby('category_pm25')
    test2 = temp.groupby('category_pm10')

    # Need to write a program to give appropriate values to a,b,c and d
    key25 = []
    key10 = []

    for i in range(0, len(list(test1))):
        key25.append(list(test1)[i][0])

    for i in range(0, len(list(test2))):
        key10.append(list(test2)[i][0])

    val25 = []
    val10 = []

    for i in range(0, len(key25)):
        val25.append(list(test1)[i][1].shape[0])

    for i in range(0, len(key10)):
        val10.append(list(test2)[i][1].shape[0])

    res25 = dict(zip(key25, val25))
    res10 = dict(zip(key10, val10))

    expected = ['a', 'b', 'c', 'd']

    for j in expected:
        if j not in res25.keys():
            new25 = {j: 0}
            res25.update(new25)
        else:
            pass

    for j in expected:
        if j not in res10.keys():
            new10 = {j: 0}
            res10.update(new10)
        else:
            pass

    print("Key25 is : ", key25)
    print("The list25 from algorithm is : ", res25.keys())
    print("val25 is : ", res25.values())
    print("Key10 is : ", key10)
    print("The list10 from algorithm is : ", res10.keys())
    print("Val10 is : ", res10.values())

    a = res25['a']
    b = res25['b']
    c = res25['c']
    d = res25['d']

    A = ((a + d)/(a+b+c+d)) * 100  # Accuracy of events
    if a != 0 or b != 0:
        FAR = ((b)/(a+b)) * 100  # False event forecase
    if a != 0 or c != 0:
        POD = ((a)/(a+c)) * 100  # Expected events
    try:
        CSI = ((a)/(a+b+c)) * 100  # Events and event forecasts that were hits
        pointer1 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer1 = 1
    if a != 0 or c != 0:
        FOM = ((c)/(a+c))*100  # Surprise events
    if a != 0 or b != 0:
        FOH = ((a)/(a+b))*100  # Correct event forecasts
    if b != 0 or d != 0:
        PON = ((d)/(b+d))*100  # Expected non events
        POFD = ((b)/(b+d))*100  # Unexpected non events
    if c != 0 or d != 0:
        DFR = ((c)/(c+d))*100  # False non-event forecasts
        FOCN = ((d)/(c+d))*100  # Correct non-event forecasts
    try:
        # True skill statistic (Expected events  - unexpected non-events)
        TSS = ((a)/(a+c)) - ((b)/(b+d))
        Heidke = (((a+c)*(d-b))+((a-c)*(d+b)))/(((a+c)*(c+d))+((a+b)*(b+d)))
        pointer2 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer2 = 1

    print("Performance metrics or Skill score for Very Unhealthy PM2.5 are:\n")

    print("A = ", A)
    if a != 0 or b != 0:
        print("FAR = ", FAR)
    if a != 0 or c != 0:
        print("POD = ", POD)
    if pointer1 == 0:
        print("CSI = ", CSI)
    if a != 0 or c != 0:
        print("FOM = ", FOM)
    if a != 0 or b != 0:
        print("FOH = ", FOH)
    if b != 0 or d != 0:
        print("PON = ", PON)
        print("POFD = ", POFD)
    if c != 0 or d != 0:
        print("DFR = ", DFR)
        print("FOCN = ", FOCN)
    if pointer2 == 0:
        print("TSS = ", TSS)
        print("Heidke = ", Heidke, "\n")

    a = res10['a']
    b = res10['b']
    c = res10['c']
    d = res10['d']

    A = ((a + d)/(a+b+c+d)) * 100  # Accuracy of events
    if a != 0 or b != 0:
        FAR = ((b)/(a+b)) * 100  # False event forecase
    if a != 0 or c != 0:
        POD = ((a)/(a+c)) * 100  # Expected events
    try:
        CSI = ((a)/(a+b+c)) * 100  # Events and event forecasts that were hits
        pointer1 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer1 = 1
    if a != 0 or c != 0:
        FOM = ((c)/(a+c))*100  # Surprise events
    if a != 0 or b != 0:
        FOH = ((a)/(a+b))*100  # Correct event forecasts
    if b != 0 or d != 0:
        PON = ((d)/(b+d))*100  # Expected non events
        POFD = ((b)/(b+d))*100  # Unexpected non events
    if c != 0 or d != 0:
        DFR = ((c)/(c+d))*100  # False non-event forecasts
        FOCN = ((d)/(c+d))*100  # Correct non-event forecasts
    try:
        # True skill statistic (Expected events  - unexpected non-events)
        TSS = ((a)/(a+c)) - ((b)/(b+d))
        Heidke = (((a+c)*(d-b))+((a-c)*(d+b)))/(((a+c)*(c+d))+((a+b)*(b+d)))
        pointer2 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer2 = 1

    print("Performance metrics or Skill score for Very Unhealthy PM10 are:\n")

    print("A = ", A)
    if a != 0 or b != 0:
        print("FAR = ", FAR)
    if a != 0 or c != 0:
        print("POD = ", POD)
    if pointer1 == 0:
        print("CSI = ", CSI)
    if a != 0 or c != 0:
        print("FOM = ", FOM)
    if a != 0 or b != 0:
        print("FOH = ", FOH)
    if b != 0 or d != 0:
        print("PON = ", PON)
        print("POFD = ", POFD)
    if c != 0 or d != 0:
        print("DFR = ", DFR)
        print("FOCN = ", FOCN)
    if pointer2 == 0:
        print("TSS = ", TSS)
        print("Heidke = ", Heidke, "\n")


# SCore calc for Unhealthy Conditions (very poor, severe conditions only)

def get_unhealthy_score(data):

    temp = data.copy(deep=True)

    conditions1 = [
        (temp['quality_mod_pm25'] >= 3) & (temp['quality_obs_pm25'] >= 3),
        (temp['quality_mod_pm25'] >= 3) & (temp['quality_obs_pm25'] < 3),
        (temp['quality_mod_pm25'] < 3) & (temp['quality_obs_pm25'] >= 3),
        (temp['quality_mod_pm25'] < 3) & (temp['quality_obs_pm25'] < 3)]

    choices1 = ['a', 'b', 'c', 'd']

    conditions2 = [
        (temp['quality_mod_pm10'] >= 3) & (temp['quality_obs_pm10'] >= 3),
        (temp['quality_mod_pm10'] >= 3) & (temp['quality_obs_pm10'] < 3),
        (temp['quality_mod_pm10'] < 3) & (temp['quality_obs_pm10'] >= 3),
        (temp['quality_mod_pm10'] < 3) & (temp['quality_obs_pm10'] < 3)]

    choices2 = ['a', 'b', 'c', 'd']

    temp['category_pm25'] = np.select(conditions1, choices1, default=np.nan)
    temp['category_pm10'] = np.select(conditions2, choices2, default=np.nan)

    test1 = temp.groupby('category_pm25')
    test2 = temp.groupby('category_pm10')

    # Need to write a program to give appropriate values to a,b,c and d
    key25 = []
    key10 = []

    for i in range(0, len(list(test1))):
        key25.append(list(test1)[i][0])

    for i in range(0, len(list(test2))):
        key10.append(list(test2)[i][0])

    val25 = []
    val10 = []

    for i in range(0, len(key25)):
        val25.append(list(test1)[i][1].shape[0])

    for i in range(0, len(key10)):
        val10.append(list(test2)[i][1].shape[0])

    res25 = dict(zip(key25, val25))
    res10 = dict(zip(key10, val10))

    expected = ['a', 'b', 'c', 'd']

    for j in expected:
        if j not in res25.keys():
            new25 = {j: 0}
            res25.update(new25)
        else:
            pass

    for j in expected:
        if j not in res10.keys():
            new10 = {j: 0}
            res10.update(new10)
        else:
            pass

    print("Key25 is : ", key25)
    print("The list25 from algorithm is : ", res25.keys())
    print("val25 is : ", res25.values())
    print("Key10 is : ", key10)
    print("The list10 from algorithm is : ", res10.keys())
    print("Val10 is : ", res10.values())

    a = res25['a']
    b = res25['b']
    c = res25['c']
    d = res25['d']

    A = ((a + d)/(a+b+c+d)) * 100  # Accuracy of events
    if a != 0 or b != 0:
        FAR = ((b)/(a+b)) * 100  # False event forecase
    if a != 0 or c != 0:
        POD = ((a)/(a+c)) * 100  # Expected events
    try:
        CSI = ((a)/(a+b+c)) * 100  # Events and event forecasts that were hits
        pointer1 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer1 = 1
    if a != 0 or c != 0:
        FOM = ((c)/(a+c))*100  # Surprise events
    if a != 0 or b != 0:
        FOH = ((a)/(a+b))*100  # Correct event forecasts
    if b != 0 or d != 0:
        PON = ((d)/(b+d))*100  # Expected non events
        POFD = ((b)/(b+d))*100  # Unexpected non events
    if c != 0 or d != 0:
        DFR = ((c)/(c+d))*100  # False non-event forecasts
        FOCN = ((d)/(c+d))*100  # Correct non-event forecasts
    try:
        # True skill statistic (Expected events  - unexpected non-events)
        TSS = ((a)/(a+c)) - ((b)/(b+d))
        Heidke = (((a+c)*(d-b))+((a-c)*(d+b)))/(((a+c)*(c+d))+((a+b)*(b+d)))
        pointer2 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer2 = 1

    print("Performance metrics or Skill score for Unhealthy PM2.5 are:\n")

    print("A = ", A)
    if a != 0 or b != 0:
        print("FAR = ", FAR)
    if a != 0 or c != 0:
        print("POD = ", POD)
    if pointer1 == 0:
        print("CSI = ", CSI)
    if a != 0 or c != 0:
        print("FOM = ", FOM)
    if a != 0 or b != 0:
        print("FOH = ", FOH)
    if b != 0 or d != 0:
        print("PON = ", PON)
        print("POFD = ", POFD)
    if c != 0 or d != 0:
        print("DFR = ", DFR)
        print("FOCN = ", FOCN)
    if pointer2 == 0:
        print("TSS = ", TSS)
        print("Heidke = ", Heidke, "\n")

    a = res10['a']
    b = res10['b']
    c = res10['c']
    d = res10['d']

    A = ((a + d)/(a+b+c+d)) * 100  # Accuracy of events
    if a != 0 or b != 0:
        FAR = ((b)/(a+b)) * 100  # False event forecase
    if a != 0 or c != 0:
        POD = ((a)/(a+c)) * 100  # Expected events
    try:
        CSI = ((a)/(a+b+c)) * 100  # Events and event forecasts that were hits
        pointer1 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer1 = 1
    if a != 0 or c != 0:
        FOM = ((c)/(a+c))*100  # Surprise events
    if a != 0 or b != 0:
        FOH = ((a)/(a+b))*100  # Correct event forecasts
    if b != 0 or d != 0:
        PON = ((d)/(b+d))*100  # Expected non events
        POFD = ((b)/(b+d))*100  # Unexpected non events
    if c != 0 or d != 0:
        DFR = ((c)/(c+d))*100  # False non-event forecasts
        FOCN = ((d)/(c+d))*100  # Correct non-event forecasts
    try:
        # True skill statistic (Expected events  - unexpected non-events)
        TSS = ((a)/(a+c)) - ((b)/(b+d))
        Heidke = (((a+c)*(d-b))+((a-c)*(d+b)))/(((a+c)*(c+d))+((a+b)*(b+d)))
        pointer2 = 0
    except ZeroDivisionError:
        print("ZeroDivisionError")
        pointer2 = 1

    print("Performance metrics or Skill score for Unhealthy PM10 are:\n")

    print("A = ", A)
    if a != 0 or b != 0:
        print("FAR = ", FAR)
    if a != 0 or c != 0:
        print("POD = ", POD)
    if pointer1 == 0:
        print("CSI = ", CSI)
    if a != 0 or c != 0:
        print("FOM = ", FOM)
    if a != 0 or b != 0:
        print("FOH = ", FOH)
    if b != 0 or d != 0:
        print("PON = ", PON)
        print("POFD = ", POFD)
    if c != 0 or d != 0:
        print("DFR = ", DFR)
        print("FOCN = ", FOCN)
    if pointer2 == 0:
        print("TSS = ", TSS)
        print("Heidke = ", Heidke, "\n")
