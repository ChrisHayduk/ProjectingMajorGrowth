import warnings
import itertools
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

CleanedData = pd.read_csv('CleanedData.csv', index_col=2, low_memory=False, parse_dates=['DATE']) #Change term code column to date time when possible
del CleanedData['Unnamed: 0']

majors = CleanedData['MAJOR_CODE_1'].unique().tolist()

for major in majors:
    data = CleanedData.loc[CleanedData.MAJOR_CODE_1==major]

    data = data.convert_objects(convert_numeric=True)
    print(data.dtypes)

    data.plot(figsize=(15, 6))
    plt.show()

    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))
    print(pdq)

    warnings.filterwarnings("ignore") # specify to ignore warning messages

    for param in pdq:
        try:
            mod = ARIMA(data['CREDITS_ATTEMPTED'], order=param)

            results = mod.fit(disp=0)

            print('ARIMA{} - AIC:{}'.format(param, results.aic))
        except:
            continue

    mod = ARIMA(data['CREDITS_ATTEMPTED'], order=(0, 1, 1))

    results = mod.fit(disp=0)

    print(results.summary().tables[1])

    pred = mod.predict(params=(0.0,1.0,1.0), start=pd.to_datetime('2014-05-15'), end=18, dynamic=False)
    print(pred)
    #ax = data['2007':].plot(label='observed')
    plt.plot(pred)
    plt.show()
