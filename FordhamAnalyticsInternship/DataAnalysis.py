import warnings
import itertools
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import os
plt.style.use('fivethirtyeight')

CleanedData = pd.read_csv('CleanedData.csv', index_col=0, low_memory=False, parse_dates=['DATE']) #Change term code column to date time when possible

majors = CleanedData['MAJOR'].unique().tolist()

for major in majors:
    data = CleanedData.loc[CleanedData.MAJOR==major]
    data = data.convert_objects(convert_numeric=True)
    print(data.dtypes)

    if(len(data)>=5):
        directory = '/home/chris/Desktop/ProjectingMajorGrowth/FordhamAnalyticsInternship/Plots/' + major
        if not os.path.exists(directory):
            os.makedirs(directory)

        data['CHANGE_IN_CREDITS_ATTEMPTED'].plot(figsize=(15, 6))
        plt.ylabel('Change in Credits for ' + major)
        plt.savefig(directory + '/' + major + '_data.png')


        # Define the p, d and q parameters to take any value between 0 and 2
        p = d = q = range(0, 2)

       # Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))
        print(pdq)

        warnings.filterwarnings("ignore") # specify to ignore warning messages

        start = len(data)//2
        end = len(data)
        resultlist = []

        for param in pdq:
            try:
                mod = ARIMA(data['CHANGE_IN_CREDITS_ATTEMPTED'], order=param)

                results = mod.fit(disp=0)
                resultlist.append(results.aic)

                print('ARIMA{} - AIC:{}'.format(param, results.aic))
            except:
                continue

        try:
            index = resultlist.index(min(resultlist))
            f_pdq = pdq[index]
            final_pdq = []

            for x in f_pdq:
                final_pdq.append(float(x))

            final_pdq = tuple(final_pdq)
            print(final_pdq)
            mod = ARIMA(data['CHANGE_IN_CREDITS_ATTEMPTED'], order=f_pdq)

            results = mod.fit(disp=0)

            #print(results.summary().tables[1])

            results.plot_predict(start=start, end=end, dynamic=True, plot_insample=True)
            plt.savefig(directory + '/' + major + '_projection.png')
        except:
            pass
